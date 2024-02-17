from django.db import models

# Create your models here.
class CAMS_Files(models.Model):
    filename = models.CharField(max_length=500)
    word_files = models.FileField(upload_to="Media/Resources")
    files_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.filename
    

    def delete(self, *args, **kwargs):
        # Delete the associated files if they exist
        if self.word_files:
            self.word_files.delete()
        if self.files_url:
            # Assuming files_url is not a FileField but a URLField, no need to delete it
            pass

        # Call the parent class's delete method
        super().delete(*args, **kwargs)
