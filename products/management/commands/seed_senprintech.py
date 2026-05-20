from django.core.management.base import BaseCommand

from products.models import Category, Product, ProductOption, ProductOptionChoice


class Command(BaseCommand):
    help = "Create SenPrinTech demo categories and products."

    def handle(self, *args, **options):
        categories = [
            ("Flyers", "flyers"),
            ("T-shirts", "t-shirts"),
            ("Cartes de visite", "cartes-de-visite"),
            ("Mugs", "mugs"),
            ("Stickers", "stickers"),
        ]

        for name, slug in categories:
            Category.objects.get_or_create(slug=slug, defaults={"name": name})

        products = [
            {
                "category": "flyers",
                "name": "Flyers A5 premium",
                "slug": "flyers-a5-premium",
                "description": "Flyers couleur pour promotions, evenements et lancements de marque.",
                "price": 15000,
                "image": "products/FLYERS.png",
            },
            {
                "category": "t-shirts",
                "name": "T-shirt personnalise",
                "slug": "t-shirt-personnalise",
                "description": "Impression textile nette pour equipes, boutiques et campagnes.",
                "price": 8000,
                "image": "products/T-Shirt.png",
            },
            {
                "category": "cartes-de-visite",
                "name": "Cartes de visite business",
                "slug": "cartes-de-visite-business",
                "description": "Cartes professionnelles au rendu propre pour laisser une premiere impression solide.",
                "price": 12000,
                "image": "products/cartevisite.png",
            },
            {
                "category": "mugs",
                "name": "Mug marque",
                "slug": "mug-marque",
                "description": "Mug personnalise pour cadeaux clients, bureaux et produits derives.",
                "price": 6500,
                "image": "products/IMAGETSHIRT.png",
            },
            {
                "category": "stickers",
                "name": "Pack stickers vinyle",
                "slug": "pack-stickers-vinyle",
                "description": "Stickers resistants pour packaging, laptops, vitrines et operations terrain.",
                "price": 5000,
                "image": "products/green.jpg",
            },
        ]

        created_count = 0
        updated_count = 0
        for item in products:
            category = Category.objects.get(slug=item.pop("category"))
            product, created = Product.objects.update_or_create(
                slug=item["slug"],
                defaults={**item, "category": category, "available": True},
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        option_specs = {
            "flyers-a5-premium": [
                ("Format", "format", "select", True, [("A6", "a6", 0), ("A5", "a5", 2000), ("A4", "a4", 5000)]),
                ("Quantite", "quantite", "select", True, [("100", "100", 0), ("250", "250", 7000), ("500", "500", 15000), ("1000", "1000", 28000), ("2000", "2000", 50000)]),
                ("Type de papier", "papier", "select", True, [("Standard", "standard", 0), ("Premium", "premium", 3000), ("Brillant", "brillant", 4000), ("Mat", "mat", 4000)]),
                ("Impression", "impression", "select", True, [("Recto", "recto", 0), ("Recto-verso", "recto-verso", 6000)]),
                ("Finition", "finition", "select", True, [("Aucune", "aucune", 0), ("Pelliculage mat", "pelliculage-mat", 7000), ("Pelliculage brillant", "pelliculage-brillant", 7000)]),
                ("Fichier design/logo", "fichier", "file", True, []),
            ],
            "cartes-de-visite-business": [
                ("Quantite", "quantite", "select", True, [("100", "100", 0), ("250", "250", 6000), ("500", "500", 13000), ("1000", "1000", 24000)]),
                ("Papier", "papier", "select", True, [("Standard", "standard", 0), ("Premium", "premium", 2500), ("Luxe", "luxe", 6000)]),
                ("Impression", "impression", "select", True, [("Recto", "recto", 0), ("Recto-verso", "recto-verso", 4000)]),
                ("Finition", "finition", "select", True, [("Mat", "mat", 0), ("Brillant", "brillant", 2500), ("Soft touch", "soft-touch", 6000)]),
                ("Coins", "coins", "select", True, [("Droits", "droits", 0), ("Arrondis", "arrondis", 3500)]),
                ("Fichier design/logo", "fichier", "file", True, []),
            ],
            "t-shirt-personnalise": [
                ("Taille", "taille", "select", True, [("S", "s", 0), ("M", "m", 0), ("L", "l", 0), ("XL", "xl", 1000), ("XXL", "xxl", 1500)]),
                ("Couleur", "couleur", "select", True, [("Blanc", "blanc", 0), ("Noir", "noir", 1000), ("Gris", "gris", 1000), ("Bleu", "bleu", 1000), ("Rouge", "rouge", 1000)]),
                ("Quantite", "quantite", "select", True, [("1", "1", 0), ("5", "5", 30000), ("10", "10", 58000), ("25", "25", 135000), ("50", "50", 250000)]),
                ("Zone d'impression", "zone-impression", "select", True, [("Devant", "devant", 0), ("Dos", "dos", 0), ("Devant + dos", "devant-dos", 5000)]),
                ("Technique", "technique", "select", True, [("Flex", "flex", 0), ("Serigraphie", "serigraphie", 4000), ("Sublimation", "sublimation", 5000)]),
                ("Logo/image", "fichier", "file", True, []),
                ("Texte personnalise", "texte", "text", False, []),
            ],
            "mug-marque": [
                ("Quantite", "quantite", "select", True, [("1", "1", 0), ("5", "5", 22000), ("10", "10", 42000), ("25", "25", 95000), ("50", "50", 175000)]),
                ("Couleur", "couleur", "select", True, [("Blanc", "blanc", 0), ("Noir", "noir", 1000), ("Rouge", "rouge", 1000)]),
                ("Impression", "impression", "select", True, [("Une face", "une-face", 0), ("Deux faces", "deux-faces", 1500), ("Panorama", "panorama", 2500)]),
                ("Image/logo", "fichier", "file", True, []),
                ("Texte personnalise", "texte", "text", False, []),
            ],
            "pack-stickers-vinyle": [
                ("Format", "format", "select", True, [("Petit", "petit", 0), ("Moyen", "moyen", 2500), ("Grand", "grand", 5000), ("Personnalise", "personnalise", 8000)]),
                ("Quantite", "quantite", "select", True, [("50", "50", 0), ("100", "100", 3500), ("250", "250", 9000), ("500", "500", 16000), ("1000", "1000", 30000)]),
                ("Matiere", "matiere", "select", True, [("Papier", "papier", 0), ("Vinyle", "vinyle", 4500), ("Transparent", "transparent", 6000)]),
                ("Forme", "forme", "select", True, [("Rond", "rond", 0), ("Carre", "carre", 0), ("Rectangle", "rectangle", 0), ("Personnalise", "personnalise", 4500)]),
                ("Finition", "finition", "select", True, [("Mat", "mat", 0), ("Brillant", "brillant", 2500)]),
                ("Fichier design/logo", "fichier", "file", True, []),
            ],
        }

        for product_slug, options in option_specs.items():
            product = Product.objects.get(slug=product_slug)
            for option_index, (name, code, input_type, required, choices) in enumerate(options, start=1):
                option, _ = ProductOption.objects.update_or_create(
                    product=product,
                    code=code,
                    defaults={
                        "name": name,
                        "input_type": input_type,
                        "required": required,
                        "sort_order": option_index,
                    },
                )
                for choice_index, (label, value, price_delta) in enumerate(choices, start=1):
                    ProductOptionChoice.objects.update_or_create(
                        option=option,
                        value=value,
                        defaults={
                            "label": label,
                            "price_delta": price_delta,
                            "sort_order": choice_index,
                        },
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"SenPrinTech demo ready: {created_count} created, {updated_count} updated."
            )
        )
