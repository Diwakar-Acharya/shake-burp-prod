from django.db import models

class Product(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    badge = models.CharField(max_length=50, blank=True, null=True)
    badge_class = models.CharField(max_length=50, blank=True, null=True, default="badge-w")
    desc = models.TextField(blank=True, null=True)
    specs = models.JSONField(default=list, blank=True, help_text="List of specifications, e.g. [\"900ml\", \"36hr cold\"]")
    color = models.CharField(max_length=7, help_text="Hex color code, e.g. #ff0000")
    svg = models.TextField(blank=True, null=True, help_text="Inline SVG code representing the bottle design")
    image = models.ImageField(upload_to="products/", blank=True, null=True, help_text="Main photo of the product")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} Image"
