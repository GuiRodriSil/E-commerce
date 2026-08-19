from app.database import Base, SessionLocal, engine
from app.models import Category, Product


PRODUCTS = [
    {
        "name": "Notebook Pro 14",
        "category": "Eletronicos",
        "description": "Notebook ultrafino com tela Full HD e bateria para longas jornadas.",
        "price": 2499.90,
        "stock": 12,
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Fone Bluetooth X9",
        "category": "Audio",
        "description": "Fones com cancelamento de ruido e audio imersivo para musica e chamadas.",
        "price": 399.99,
        "stock": 28,
        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Smartwatch Active",
        "category": "Acessorios",
        "description": "Relogio inteligente com monitoramento de saude e notificacoes.",
        "price": 799.00,
        "stock": 18,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Camera Mirrorless",
        "category": "Fotografia",
        "description": "Camera leve com foco rapido, gravacao 4K e alta qualidade de imagem.",
        "price": 1899.00,
        "stock": 9,
        "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Mesa de Escritorio",
        "category": "Casa",
        "description": "Mesa moderna com acabamento premium, ideal para home office.",
        "price": 679.90,
        "stock": 7,
        "image_url": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Cafeteira Premium",
        "category": "Casa",
        "description": "Cafeteira com preparo rapido e design sofisticado para o dia a dia.",
        "price": 449.90,
        "stock": 15,
        "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=80",
    },
]


def seed_products():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    created = 0
    try:
        for product_data in PRODUCTS:
            category = db.query(Category).filter(Category.name == product_data["category"]).first()
            if not category:
                category = Category(name=product_data["category"])
                db.add(category)
                db.flush()

            existing_product = db.query(Product).filter(Product.name == product_data["name"]).first()
            if existing_product:
                continue

            db.add(
                Product(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    stock=product_data["stock"],
                    image_url=product_data["image_url"],
                    category_id=category.id,
                    is_active=True,
                )
            )
            created += 1

        db.commit()
        print(f"Produtos criados: {created}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_products()
