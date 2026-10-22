
from django.db import models


class Department(models.Model):
    organization = models.ForeignKey(
        "common.Organization",
        on_delete=models.PROTECT,
        related_name="departments",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "name"),
                name="unique_department_name_per_organization",
            ),
        ]

    def __str__(self):
        return self.name
