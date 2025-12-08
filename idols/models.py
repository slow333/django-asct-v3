from django.db import models
from django.urls import reverse

class Idol(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='idol_images/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail:
            from PIL import Image
            from io import BytesIO
            from django.core.files.base import ContentFile

            img = Image.open(self.image)
            if img.height > 200 or img.width > 200:
                img.thumbnail((200, 200))
            thumb_io = BytesIO()
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(thumb_io, format='JPEG')
            self.thumbnail.save(f'thumbnail_{self.image.name}', ContentFile(thumb_io.getvalue()), save=False)
            super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('idol-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
    
