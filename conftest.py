"""
conftest.py - Configuration centralisée pour tous les tests pytest
Contient les fixtures réutilisables pour les différentes applications
"""

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date
from shop.models import (
    CategorieEtablissement,
    CategorieProduit,
    Etablissement,
    Produit,
    Favorite,
)
from customer.models import (
    Customer,
    CodePromotionnel,
    Panier,
    ProduitPanier,
    Commande,
    PasswordResetToken,
)
from contact.models import Contact, NewsLetter
from cities_light.models import City, Country


# ==================== FIXTURES UTILISATEUR ====================

@pytest.fixture
def user_data():
    """Données de test pour créer un utilisateur"""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test@123456',
        'first_name': 'Jean',
        'last_name': 'Dupont',
    }


@pytest.fixture
def user(user_data, db):
    """Crée un utilisateur de test"""
    user = User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
    )
    return user


@pytest.fixture
def another_user(db):
    """Crée un second utilisateur de test"""
    return User.objects.create_user(
        username='anotheruser',
        email='another@example.com',
        password='Test@654321',
    )


# ==================== FIXTURES GÉOLOCALISATION ====================

@pytest.fixture
def city(db):
    """Crée une ville de test (pour les relations ForeignKey)"""
    # Créer d'abord un pays
    country, _ = Country.objects.get_or_create(
        slug='ci',
        defaults={
            'name': 'Côte d\'Ivoire',
            'name_ascii': 'Cote d\'Ivoire',
            'code2': 'CI',
            'code3': 'CIV',
            'phone': '225',
        }
    )
    
    # Ensuite créer une ville avec ce pays
    city, _ = City.objects.get_or_create(
        slug='abidjan',
        defaults={
            'name': 'Abidjan',
            'country': country,
        }
    )
    return city


# ==================== FIXTURES SHOP ====================

@pytest.fixture
def categorie_etablissement(db):
    """Crée une catégorie d'établissement de test"""
    return CategorieEtablissement.objects.create(
        nom="Restaurants",
        description="Catégorie des restaurants",
        status=True,
    )


@pytest.fixture
def categorie_produit(db, categorie_etablissement):
    """Crée une catégorie de produit de test"""
    return CategorieProduit.objects.create(
        nom="Plats Principaux",
        description="Plats principaux du menu",
        categorie=categorie_etablissement,
        status=True,
    )


@pytest.fixture
def etablissement(db, user, categorie_etablissement, city):
    """Crée un établissement (vendeur) de test"""
    return Etablissement.objects.create(
        user=user,
        nom="Restaurant le Delice",
        description="Le meilleur restaurant de la ville",
        logo="test_logo.jpg",
        couverture="test_couverture.jpg",
        categorie=categorie_etablissement,
        nom_du_responsable="Jean",
        prenoms_duresponsable="Dupont",
        ville=city,
        adresse="123 Rue de Paris",
        pays="Côte d'Ivoire",
        contact_1="+225 01 23 45 67",
        email="restaurant@example.com",
        status=True,
    )


@pytest.fixture
def produit_sans_promo(db, categorie_produit, categorie_etablissement, etablissement):
    """Crée un produit sans promotion"""
    return Produit.objects.create(
        nom="Attiéké Poisson",
        description="Attiéké avec poisson frais",
        description_deal="Délicieux attiéké",
        prix=5000,
        prix_promotionnel=0,
        quantite=100,
        date_debut_promo=None,
        date_fin_promo=None,
        categorie_etab=categorie_etablissement,
        categorie=categorie_produit,
        etablissement=etablissement,
        status=True,
        super_deal=False,
    )


@pytest.fixture
def produit_avec_promo_active(db, categorie_produit, categorie_etablissement, etablissement):
    """Crée un produit avec promotion active"""
    today = date.today()
    return Produit.objects.create(
        nom="Placali Sauce",
        description="Placali avec sauce graine",
        description_deal="Promotion spéciale",
        prix=6000,
        prix_promotionnel=4500,
        quantite=50,
        date_debut_promo=today - timedelta(days=1),  # Promotion commencée hier
        date_fin_promo=today + timedelta(days=30),   # Expire dans 30 jours
        categorie_etab=categorie_etablissement,
        categorie=categorie_produit,
        etablissement=etablissement,
        status=True,
        super_deal=False,
    )


@pytest.fixture
def produit_avec_promo_expirée(db, categorie_produit, categorie_etablissement, etablissement):
    """Crée un produit avec promotion expirée"""
    today = date.today()
    return Produit.objects.create(
        nom="Riz Sauce",
        description="Riz avec sauce",
        description_deal="Ancienne promotion",
        prix=4000,
        prix_promotionnel=3000,
        quantite=100,
        date_debut_promo=today - timedelta(days=60),
        date_fin_promo=today - timedelta(days=1),    # Expirée hier
        categorie_etab=categorie_etablissement,
        categorie=categorie_produit,
        etablissement=etablissement,
        status=True,
        super_deal=False,
    )


@pytest.fixture
def produit_super_deal(db, categorie_produit, categorie_etablissement, etablissement):
    """Crée un super deal (produit vedette)"""
    today = date.today()
    return Produit.objects.create(
        nom="Menu Spécial VIP",
        description="Menu complet incluant entrée, plat et dessert",
        description_deal="Super deal du jour",
        prix=15000,
        prix_promotionnel=10000,
        quantite=30,
        date_debut_promo=today - timedelta(days=1),
        date_fin_promo=today + timedelta(days=7),
        categorie_etab=categorie_etablissement,
        categorie=categorie_produit,
        etablissement=etablissement,
        status=True,
        super_deal=True,
    )


# ==================== FIXTURES CUSTOMER ====================

@pytest.fixture
def customer(db, user, city):
    """Crée un client de test"""
    return Customer.objects.create(
        user=user,
        adresse="456 Avenue de la Paix",
        contact_1="+225 09 87 65 43",
        contact_2="+225 07 12 34 56",
        ville=city,
        pays="Côte d'Ivoire",
        status=True,
    )


@pytest.fixture
def code_promotionnel(db, produit_sans_promo):
    """Crée un code promotionnel de test"""
    code = CodePromotionnel.objects.create(
        libelle="NOEL2024",
        etat=True,
        date_fin=date.today() + timedelta(days=30),
        reduction=0.15,  # 15% de réduction
        nombre_u=100,
        code_promo="NOEL2024",
        status=True,
    )
    code.forfait.add(produit_sans_promo)
    return code


@pytest.fixture
def panier(db, customer):
    """Crée un panier de test"""
    return Panier.objects.create(
        customer=customer,
        status=True,
    )


@pytest.fixture
def produit_panier(db, panier, produit_sans_promo):
    """Ajoute un produit au panier"""
    return ProduitPanier.objects.create(
        produit=produit_sans_promo,
        panier=panier,
        quantite=2,
        status=True,
    )


@pytest.fixture
def commande(db, customer):
    """Crée une commande de test"""
    return Commande.objects.create(
        customer=customer,
        prix_total=10000,
        status=True,
    )


@pytest.fixture
def password_reset_token(db, user):
    """Crée un token de réinitialisation de mot de passe"""
    from django.utils.crypto import get_random_string
    token_value = get_random_string(100)
    return PasswordResetToken.objects.create(
        user=user,
        token=token_value,
    )


# ==================== FIXTURES CONTACT ====================

@pytest.fixture
def contact_message(db):
    """Crée un message de contact de test"""
    return Contact.objects.create(
        nom="Marie Martin",
        sujet="Question sur les produits",
        email="marie@example.com",
        message="Je voudrais connaître les conditions de livraison.",
        status=True,
    )


@pytest.fixture
def newsletter_subscriber(db):
    """Crée un abonné à la newsletter"""
    return NewsLetter.objects.create(
        email="subscriber@example.com",
        status=True,
    )


# ==================== FIXTURES UTILITIES ====================

@pytest.fixture
def favorite(db, user, produit_sans_promo):
    """Crée un produit favori"""
    return Favorite.objects.create(
        user=user,
        produit=produit_sans_promo,
    )


@pytest.fixture
def api_client():
    """Retourne un client API pour les tests d'intégration"""
    from rest_framework.test import APIClient
    return APIClient()
