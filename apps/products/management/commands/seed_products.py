from django.core.management.base import BaseCommand
from apps.products.models import Product

class Command(BaseCommand):
    help = "Seeds initial high-end shaker bottle products into the database"

    def handle(self, *args, **options):
        products_data = [
            {
                "slug": "vortex-pro-shaker-900ml",
                "name": "Vortex Pro Shaker 900ml",
                "price": 34.99,
                "badge": "Bestseller",
                "badge_class": "badge-r",
                "desc": "Double-wall vacuum insulated 316 stainless steel shaker bottle with leakproof magnetic cap and UV DTF custom artwork.",
                "specs": ["900ml", "36hr Cold", "316 Stainless Steel", "UV DTF Printed"],
                "color": "#D10000",
                "svg": """<rect x="25" y="10" width="40" height="15" rx="4" fill="#333"/><rect x="20" y="25" width="50" height="160" rx="10" fill="#D10000"/>""",
                "is_active": True
            },
            {
                "slug": "stealth-titanium-900ml",
                "name": "Stealth Titanium Shaker 900ml",
                "price": 39.99,
                "badge": "Pro Grade",
                "badge_class": "badge-w",
                "desc": "Aerospace-grade titanium coated shaker with silent agitating mesh and sweat-proof matte finish.",
                "specs": ["900ml", "Titanium Coated", "Silent Agitator", "Sweat Proof"],
                "color": "#232325",
                "svg": """<rect x="25" y="10" width="40" height="15" rx="4" fill="#111"/><rect x="20" y="25" width="50" height="160" rx="10" fill="#232325"/>""",
                "is_active": True
            },
            {
                "slug": "cyber-neon-750ml",
                "name": "Cyber Neon Shaker 750ml",
                "price": 29.99,
                "badge": "Limited Edition",
                "badge_class": "badge-w",
                "desc": "Vibrant cyan cyber-themed insulated shaker bottle with luminescent accent rings and non-slip rubber base.",
                "specs": ["750ml", "24hr Cold", "Luminescent Accent", "Non-slip Base"],
                "color": "#00E5FF",
                "svg": """<rect x="25" y="10" width="40" height="15" rx="4" fill="#00ACC1"/><rect x="20" y="25" width="50" height="160" rx="10" fill="#00E5FF"/>""",
                "is_active": True
            },
            {
                "slug": "matte-black-900ml",
                "name": "Shake&Burp Matte Black 900ml",
                "price": 39.99,
                "badge": "Hot",
                "badge_class": "badge-r",
                "desc": "Ultra-sleek stealth black insulated shaker bottle featuring high-grip texture and precision measurement markings.",
                "specs": ["900ml", "Double Wall", "Laser Engraved", "BPA Free"],
                "color": "#1A1A1A",
                "svg": """<rect x="25" y="10" width="40" height="15" rx="4" fill="#000"/><rect x="20" y="25" width="50" height="160" rx="10" fill="#1A1A1A"/>""",
                "is_active": True
            },
            {
                "slug": "solar-gold-750ml",
                "name": "Solar Gold Insulated Shaker 750ml",
                "price": 32.99,
                "badge": "New",
                "badge_class": "badge-w",
                "desc": "Premium metallic gold electroplated finish with dual-stage filter for clump-free protein shakes.",
                "specs": ["750ml", "Electroplated Gold", "Dual Stage Filter", "Leak Guard"],
                "color": "#FFB300",
                "svg": """<rect x="25" y="10" width="40" height="15" rx="4" fill="#FF8F00"/><rect x="20" y="25" width="50" height="160" rx="10" fill="#FFB300"/>""",
                "is_active": True
            },
            {
                "slug": "crimson-phantom-1000ml",
                "name": "Crimson Phantom Shaker 1000ml",
                "price": 44.99,
                "badge": "Ultra",
                "badge_class": "badge-r",
                "desc": "1-Liter maximum capacity endurance shaker built for extreme performance athletes and long workouts.",
                "specs": ["1000ml (1L)", "48hr Cold Insulation", "Heavy Duty Steel", "Carabiner Loop"],
                "color": "#FF1744",
                "svg": """<rect x="25" y="10" width="40" height="15" rx="4" fill="#D50000"/><rect x="20" y="25" width="50" height="160" rx="10" fill="#FF1744"/>""",
                "is_active": True
            }
        ]

        count = 0
        for item in products_data:
            obj, created = Product.objects.update_or_create(
                slug=item["slug"],
                defaults=item
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {count} new products into database!"))
