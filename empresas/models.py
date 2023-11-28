from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

class Empresas(models.Model):
    empresa = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Empresas"    

    def __str__(self):
        return self.empresa

class Internos(models.Model):
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    numero_interno = models.PositiveSmallIntegerField()
    chapa_mop = models.CharField(max_length=8)
   

    class Meta:
        verbose_name_plural = "Internos"    
    
    def __str__(self):
        return f"Interno {self.numero_interno}-Empresa: {self.empresa.empresa} "
    

class Desinfeccion(models.Model):
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    numero_interno = models.PositiveSmallIntegerField()
    chapa_mop = models.CharField(max_length=8)
    fecha_realizacion = models.DateField()
    fecha_vencimiento = models.DateField()
    desinfeccion_pdf = models.FileField(upload_to='desinfecciones/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Desinfecciones"    
    

    def save(self, *args, **kwargs):
        # Verificar si la fecha de vencimiento está a 7 días
        dias_hasta_vencimiento = (self.fecha_vencimiento - timezone.now().date()).days
        if dias_hasta_vencimiento == 7:
            # Enviar correo electrónico
            self.enviar_correo_vencimiento()

        super().save(*args, **kwargs)

    def enviar_correo_vencimiento(self):
        subject = 'Recordatorio: Vencimiento de Desinfección'
        message = f"La desinfección número {self.numero_interno} para la empresa {self.empresa} está programada para vencer en 7 días. Fecha de realización: {self.fecha_realizacion}, Fecha de vencimiento: {self.fecha_vencimiento}."
        from_email = settings.EMAIL_HOST_USER
        to_email = "leimgruberguille@gmail.com"  # Reemplaza con tu dirección de correo electrónico

        send_mail(subject, message, from_email, [to_email])

    def __str__(self):
        return f'Desinfeccion {self.numero_interno} - {self.empresa}'








    


class Actas(models.Model):
    numero_de_acta = models.CharField(max_length=12)
    fecha = models.DateField()
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    interno = models.PositiveSmallIntegerField()
    descripcion = models.CharField(max_length=300)
    intimacion_choices = [('si', 'Sí'), ('no', 'No')]
    intimacion = models.CharField(max_length=2, choices=intimacion_choices)
    horas_intimacion_choices = [(24, '24 horas'), (48, '48 horas'), (72, '72 horas')]
    horas_intimacion = models.PositiveSmallIntegerField(choices=horas_intimacion_choices)
    acta_pdf = models.FileField(upload_to='actas/')

    class Meta:
        verbose_name_plural = "Actas"    

    def __str__(self):
        return f"Acta {self.numero_de_acta} - Empresa: {self.empresa.empresa} - Interno: {self.interno}"
    



@receiver(post_save, sender=Actas)
def send_email_on_new_acta(sender, instance, created, **kwargs):
    if created:
        subject = "Nueva Acta Creada"
        message = f"Se ha creado una nueva acta con el número {instance.numero_de_acta} de la empresa {instance.empresa.empresa} del interno {instance.interno} el {instance.fecha} posee una intimación de {instance.horas_intimacion}."
        from_email = settings.EMAIL_HOST_USER  # Debe ser una dirección de correo válida configurada en tus settings
        recipient_list = [
            "guillermo@sierrasdecalamuchita.com",
            "marinacaballero25@gmail.com",
            "waltermorrie@gmail.com",
            "tallersancarlos77@gmail.com",
            "leimgruberguille@gmail.com"
        ]  

        send_mail(subject, message, from_email, recipient_list)



class Rectificaciones(models.Model):
    numero_rectificacion = models.CharField(max_length=12)
    fecha = models.DateField()
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    interno = models.PositiveSmallIntegerField()
    numero_acta = models.CharField(max_length=12)
    rectificacion_pdf = models.FileField(upload_to='rectificaciones/')

    class Meta:
        verbose_name_plural = "Rectificaciones"

    def __str__(self):
        return f"Acta {self.numero_rectificacion} - Empresa: {self.empresa.empresa} - Interno: {self.interno}"
    
@receiver(post_save, sender=Rectificaciones)
def send_email_on_new_acta(sender, instance, created, **kwargs):
    if created:
        subject = "Nueva Contra Acta Creada"
        message = f"Se ha creado una nueva Contra Acta con el número {instance.numero_rectificacion} de la empresa {instance.empresa.empresa} del interno {instance.interno} el dia {instance.fecha}."
        from_email = settings.EMAIL_HOST_USER  # Debe ser una dirección de correo válida configurada en tus settings
        recipient_list = ["guillermo@sierrasdecalamuchita.com", "marinacaballero25@gmail.com", "waltermorrie@gmail.com","tallersancarlos77@gmail.com","leimgruberguille@gmail.com"]  # Agrega aquí las direcciones de correo a las que deseas enviar el mensaje

        send_mail(subject, message, from_email, recipient_list)
