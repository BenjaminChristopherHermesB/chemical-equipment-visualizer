from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class EquipmentDataset(models.Model):
    """
    Model to store uploaded CSV datasets and processed results.
    Automatically manages history (keeps only last 5 datasets per user).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Store processed data as JSON
    raw_data = models.JSONField(help_text="Original CSV data as list of dictionaries")
    summary_stats = models.JSONField(help_text="Computed summary statistics")
    
    # Metadata
    row_count = models.IntegerField(default=0)
    equipment_types = models.JSONField(default=list, help_text="List of equipment types")
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Equipment Dataset"
        verbose_name_plural = "Equipment Datasets"
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def cleanup_old_datasets(cls, user, keep_count=5):
        """
        Keep only the most recent 'keep_count' datasets for the user.
        Delete older ones.
        """
        datasets = cls.objects.filter(user=user).order_by('-uploaded_at')
        if datasets.count() > keep_count:
            old_datasets = datasets[keep_count:]
            for dataset in old_datasets:
                dataset.delete()


@receiver(post_save, sender=EquipmentDataset)
def dataset_post_save(sender, instance, created, **kwargs):
    """
    Signal to auto-cleanup old datasets after each save.
    """
    if created:
        EquipmentDataset.cleanup_old_datasets(instance.user, keep_count=5)
