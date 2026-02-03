"""Tests pour l'application shop - Modèles et logique métier"""

import pytest
import datetime
from unittest.mock import patch, MagicMock
from shop.models import Produit, Favorite
from customer.models import ProduitPanier, Panier


pytestmark = pytest.mark.django_db


class TestProduitPrixLogic:
    """
    Test suite pour la logique de calcul des prix des produits
    Avec et sans promotions
    """

    @pytest.mark.unit
    def test_produit_prix_sans_promotion(self, produit_sans_promo):
        """
        Arrange: Un produit sans promotion
        Act: Récupérer le prix du produit
        Assert: Le prix normal doit être utilisé
        """
        # Arrange
        produit = produit_sans_promo
        
        # Act
        prix = produit.prix
        is_promo_active = produit.check_promotion
        
        # Assert
        assert prix == 5000
        assert is_promo_active is False
        assert produit.prix_promotionnel == 0

    @pytest.mark.unit
    def test_produit_avec_promotion_active(self, produit_avec_promo_active):
        """
        Arrange: Un produit avec promotion actuellement active
        Act: Vérifier la promotion
        Assert: La promotion doit être active
        """
        # Arrange
        produit = produit_avec_promo_active
        
        # Act
        is_promo_active = produit.check_promotion
        
        # Assert
        assert is_promo_active is True
        assert produit.prix_promotionnel == 4500
        assert produit.prix == 6000

    @pytest.mark.unit
    def test_produit_avec_promotion_expirée(self, produit_avec_promo_expirée):
        """
        Arrange: Un produit avec promotion expirée
        Act: Vérifier la promotion
        Assert: La promotion ne doit pas être active
        """
        # Arrange
        produit = produit_avec_promo_expirée
        
        # Act
        is_promo_active = produit.check_promotion
        
        # Assert
        assert is_promo_active is False
        assert produit.prix_promotionnel == 3000
        # Le prix normal doit être utilisé puisque promo est expirée

    @pytest.mark.unit
    def test_produit_promotion_pas_commencée(self, db, categorie_produit, 
                                             categorie_etablissement, etablissement):
        """
        Arrange: Un produit avec promotion future
        Act: Vérifier la promotion
        Assert: La promotion ne doit pas être active (elle commence demain)
        """
        # Arrange
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        in_30_days = tomorrow + datetime.timedelta(days=30)
        
        produit = Produit.objects.create(
            nom="Futur Deal",
            description="Promotion future",
            description_deal="Promo demain",
            prix=10000,
            prix_promotionnel=7000,
            date_debut_promo=tomorrow,
            date_fin_promo=in_30_days,
            categorie=categorie_produit,
            categorie_etab=categorie_etablissement,
            etablissement=etablissement,
            status=True,
        )
        
        # Act
        is_promo_active = produit.check_promotion
        
        # Assert
        assert is_promo_active is False

    @pytest.mark.unit
    def test_produit_panier_total_sans_promotion(self, produit_sans_promo, panier):
        """
        Arrange: Un panier avec un produit sans promotion (quantité: 2)
        Act: Calculer le total du produit en panier
        Assert: Total = prix * quantité
        """
        # Arrange
        quantite = 2
        produit_panier = ProduitPanier.objects.create(
            produit=produit_sans_promo,
            panier=panier,
            quantite=quantite,
            status=True,
        )
        
        # Act
        total = produit_panier.total
        
        # Assert
        expected_total = produit_sans_promo.prix * quantite
        assert total == expected_total
        assert total == 10000  # 5000 * 2

    @pytest.mark.unit
    def test_produit_panier_total_avec_promotion_active(self, 
                                                        produit_avec_promo_active, 
                                                        panier):
        """
        Arrange: Un panier avec un produit en promotion active (quantité: 3)
        Act: Calculer le total du produit en panier
        Assert: Total = prix_promotionnel * quantité
        """
        # Arrange
        quantite = 3
        produit_panier = ProduitPanier.objects.create(
            produit=produit_avec_promo_active,
            panier=panier,
            quantite=quantite,
            status=True,
        )
        
        # Act
        total = produit_panier.total
        
        # Assert
        expected_total = produit_avec_promo_active.prix_promotionnel * quantite
        assert total == expected_total
        assert total == 13500  # 4500 * 3

    @pytest.mark.unit
    def test_produit_panier_total_avec_promotion_expirée(self, 
                                                         produit_avec_promo_expirée, 
                                                         panier):
        """
        Arrange: Un panier avec un produit avec promotion expirée
        Act: Calculer le total du produit en panier
        Assert: Le prix normal doit être utilisé (promotion expirée)
        """
        # Arrange
        quantite = 5
        produit_panier = ProduitPanier.objects.create(
            produit=produit_avec_promo_expirée,
            panier=panier,
            quantite=quantite,
            status=True,
        )
        
        # Act
        total = produit_panier.total
        
        # Assert
        # Puisque la promo est expirée, check_promotion retourne False
        # donc le prix normal est utilisé
        expected_total = produit_avec_promo_expirée.prix * quantite
        assert total == expected_total
        assert total == 20000  # 4000 * 5

    @pytest.mark.unit
    def test_panier_total_avec_multiple_produits(self, panier, produit_sans_promo, 
                                                   produit_avec_promo_active):
        """
        Arrange: Un panier avec 2 produits différents
        Act: Calculer le total du panier
        Assert: Total = somme des totaux individuels
        """
        # Arrange
        pp1 = ProduitPanier.objects.create(
            produit=produit_sans_promo,
            panier=panier,
            quantite=1,
            status=True,
        )
        pp2 = ProduitPanier.objects.create(
            produit=produit_avec_promo_active,
            panier=panier,
            quantite=1,
            status=True,
        )
        
        # Act
        panier_total = panier.total
        
        # Assert
        expected_total = pp1.total + pp2.total
        assert panier_total == expected_total
        assert panier_total == 9500  # 5000 + 4500

    @pytest.mark.unit
    def test_panier_total_with_coupon_15_percent(self, panier, code_promotionnel, 
                                                  produit_sans_promo):
        """
        Arrange: Un panier avec un coupon 15% de réduction
        Act: Calculer le total avec coupon
        Assert: Total = total_original - (total_original * 0.15)
        """
        # Arrange
        panier.coupon = code_promotionnel
        panier.save()
        
        ProduitPanier.objects.create(
            produit=produit_sans_promo,
            panier=panier,
            quantite=2,
            status=True,
        )
        
        # Act
        total_without_coupon = panier.total
        total_with_coupon = panier.total_with_coupon
        
        # Assert
        reduction = code_promotionnel.reduction * total_without_coupon
        expected_total_with_coupon = int(total_without_coupon - reduction)
        
        assert total_without_coupon == 10000
        assert total_with_coupon == expected_total_with_coupon
        assert total_with_coupon == 8500  # 10000 - (10000 * 0.15)


class TestFavoriteLogic:
    """Tests pour la logique des produits favoris"""

    @pytest.mark.unit
    def test_add_favorite(self, user, produit_sans_promo):
        """
        Arrange: Un utilisateur et un produit
        Act: Ajouter le produit aux favoris
        Assert: Le favori doit être créé
        """
        # Arrange & Act
        favorite, created = Favorite.objects.get_or_create(
            user=user,
            produit=produit_sans_promo
        )
        
        # Assert
        assert created is True
        assert favorite.user == user
        assert favorite.produit == produit_sans_promo

    @pytest.mark.unit
    def test_favorite_unique_constraint(self, user, produit_sans_promo):
        """
        Arrange: Un favori déjà existant
        Act: Essayer d'ajouter le même favori
        Assert: Doit récupérer l'existant (pas de doublon)
        """
        # Arrange
        favorite1 = Favorite.objects.create(user=user, produit=produit_sans_promo)
        
        # Act
        favorite2, created = Favorite.objects.get_or_create(
            user=user,
            produit=produit_sans_promo
        )
        
        # Assert
        assert created is False
        assert favorite1.id == favorite2.id

    @pytest.mark.unit
    def test_remove_favorite(self, user, produit_sans_promo):
        """
        Arrange: Un favori existant
        Act: Supprimer le favori
        Assert: Le favori doit être supprimé
        """
        # Arrange
        Favorite.objects.create(user=user, produit=produit_sans_promo)
        
        # Act
        count_before = Favorite.objects.count()
        Favorite.objects.filter(user=user, produit=produit_sans_promo).delete()
        count_after = Favorite.objects.count()
        
        # Assert
        assert count_before == 1
        assert count_after == 0

    @pytest.mark.unit
    def test_user_multiple_favorites(self, user, produit_sans_promo, 
                                     produit_avec_promo_active, produit_super_deal):
        """
        Arrange: Un utilisateur avec plusieurs favoris
        Act: Récupérer tous les favoris de l'utilisateur
        Assert: L'utilisateur doit avoir 3 favoris
        """
        # Arrange
        Favorite.objects.create(user=user, produit=produit_sans_promo)
        Favorite.objects.create(user=user, produit=produit_avec_promo_active)
        Favorite.objects.create(user=user, produit=produit_super_deal)
        
        # Act
        user_favorites = Favorite.objects.filter(user=user)
        
        # Assert
        assert user_favorites.count() == 3


class TestProduitSlugGeneration:
    """Tests pour la génération automatique de slugs"""

    @pytest.mark.unit
    def test_produit_slug_auto_generation(self, categorie_produit, 
                                         categorie_etablissement, etablissement):
        """
        Arrange: Créer un nouveau produit sans slug
        Act: Sauvegarder le produit
        Assert: Un slug unique doit être généré automatiquement
        """
        # Arrange
        produit = Produit(
            nom="Test Produit Slug",
            description="Test",
            description_deal="Test",
            prix=5000,
            categorie=categorie_produit,
            categorie_etab=categorie_etablissement,
            etablissement=etablissement,
            status=True,
        )
        
        # Act
        produit.save()
        
        # Assert
        assert produit.slug is not None
        assert "test-produit-slug" in produit.slug

    @pytest.mark.unit
    def test_produit_slug_uniqueness(self, categorie_produit, 
                                    categorie_etablissement, etablissement):
        """
        Arrange: Deux produits avec le même nom
        Act: Sauvegarder les deux produits
        Assert: Chaque slug doit être unique (grâce au microsecond)
        """
        # Arrange
        produit1 = Produit.objects.create(
            nom="Produit Identique",
            description="Test",
            description_deal="Test",
            prix=5000,
            categorie=categorie_produit,
            categorie_etab=categorie_etablissement,
            etablissement=etablissement,
            status=True,
        )
        
        # Act
        produit2 = Produit.objects.create(
            nom="Produit Identique",
            description="Test",
            description_deal="Test",
            prix=5000,
            categorie=categorie_produit,
            categorie_etab=categorie_etablissement,
            etablissement=etablissement,
            status=True,
        )
        
        # Assert
        assert produit1.slug != produit2.slug
        assert "produit-identique" in produit1.slug
        assert "produit-identique" in produit2.slug
