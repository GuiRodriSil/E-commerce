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
    {
        "name": "Monitor UltraWide 34",
        "category": "Eletronicos",
        "description": "Monitor ultrawide para produtividade, criacao e entretenimento com mais espaco na tela.",
        "price": 1299.90,
        "stock": 10,
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Teclado Mecanico RGB",
        "category": "Acessorios",
        "description": "Teclado mecanico compacto com iluminacao RGB e resposta precisa.",
        "price": 249.90,
        "stock": 22,
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Poltrona Conforto",
        "category": "Casa",
        "description": "Poltrona confortavel com design contemporaneo para seu espaco de descanso.",
        "price": 899.90,
        "stock": 6,
        "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Caixa de Som Portatil",
        "category": "Audio",
        "description": "Caixa de som portatil com graves fortes, bateria duradoura e conexao sem fio.",
        "price": 179.90,
        "stock": 31,
        "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Tablet Vision 11",
        "category": "Eletronicos",
        "description": "Tablet leve com tela de alta definicao, desempenho fluido e bateria para o dia inteiro.",
        "price": 1199.90,
        "stock": 14,
        "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Luminaria de Mesa LED",
        "category": "Casa",
        "description": "Luminaria articulada com luz regulavel para deixar seu espaco de trabalho mais confortavel.",
        "price": 129.90,
        "stock": 24,
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Mouse Sem Fio Precision",
        "category": "Acessorios",
        "description": "Mouse ergonomico sem fio com sensor preciso e bateria de longa duracao.",
        "price": 159.90,
        "stock": 35,
        "image_url": "https://images.unsplash.com/photo-1527814050087-3793815479db?auto=format&fit=crop&w=900&q=80",
    },
    {
        "name": "Microfone Studio USB",
        "category": "Audio",
        "description": "Microfone USB com captacao nitida para reunioes, podcasts e criacao de conteudo.",
        "price": 329.90,
        "stock": 11,
        "image_url": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=900&q=80",
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
