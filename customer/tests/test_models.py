"""Tests unitaires pour les modèles du customer"""

import pytest
from datetime import timedelta
from django.utils.timezone import now
from customer.models import CodePromotionnel, Panier, ProduitPanier


pytestmark = pytest.mark.django_db


class TestCodePromotionnelModel:
    """Tests unitaires pour le modèle CodePromotionnel"""

    @pytest.mark.unit
    def test_code_promo_creation(self, db):
        """
        Arrange: Données pour créer un code promo
        Act: Créer un code promo
        Assert: Le code doit être créé avec tous les champs
        """
        # Arrange & Act
        code = CodePromotionnel.objects.create(
            libelle="PROMO_NOËL",
            etat=True,
            date_fin=now().date() + timedelta(days=30),
            reduction=0.20,  # 20% off
            nombre_u=50,
            code_promo="NOEL20",
            status=True,
        )
        
        # Assert
        assert code.id is not None
        assert code.libelle == "PROMO_NOËL"
        assert code.reduction == 0.20
        assert code.code_promo == "NOEL20"

    @pytest.mark.unit
    def test_code_promo_with_forfait(self, code_promotionnel, produit_sans_promo):
        """
        Arrange: Un code promo et un produit
        Act: Ajouter le produit au forfait du code
        Assert: Le produit doit être dans le forfait
        """
        # Act
        code_promotionnel.forfait.add(produit_sans_promo)
        
        # Assert
        assert produit_sans_promo in code_promotionnel.forfait.all()
        assert code_promotionnel.forfait.count() == 1

    @pytest.mark.unit
    def test_code_promo_multiple_produits(self, code_promotionnel, produit_sans_promo, 
                                         produit_avec_promo_active):
        """
        Arrange: Un code promo
        Act: Ajouter plusieurs produits
        Assert: Tous les produits doivent être dans le forfait
        """
        # Act
        code_promotionnel.forfait.add(produit_sans_promo)
        code_promotionnel.forfait.add(produit_avec_promo_active)
        
        # Assert
        assert code_promotionnel.forfait.count() == 2


class TestPanierModel:
    """Tests unitaires pour le modèle Panier"""

    @pytest.mark.unit
    def test_panier_creation(self, customer):
        """
        Arrange: Un client
        Act: Créer un panier
        Assert: Le panier doit être créé avec le client
        """
        # Arrange & Act
        panier = Panier.objects.create(
            customer=customer,
            status=True,
        )
        
        # Assert
        assert panier.id is not None
        assert panier.customer == customer
        assert panier.status is True

    @pytest.mark.unit
    def test_panier_total_empty(self, panier):
        """
        Arrange: Un panier vide
        Act: Calculer le total
        Assert: Le total doit être 0
        """
        # Act
        total = panier.total
        
        # Assert
        assert total == 0

    @pytest.mark.unit
    def test_panier_check_empty_true(self, panier):
        """
        Arrange: Un panier vide
        Act: Vérifier si le panier est vide
        Assert: check_empty doit retourner False
        """
        # Act
        is_empty = panier.check_empty
        
        # Assert
        assert is_empty is False

    @pytest.mark.unit
    def test_panier_check_empty_false(self, panier, produit_panier):
        """
        Arrange: Un panier avec un produit
        Act: Vérifier si le panier est vide
        Assert: check_empty doit retourner True
        """
        # Act
        is_empty = panier.check_empty
        
        # Assert
        assert is_empty is True

    @pytest.mark.unit
    def test_panier_total_with_coupon_discount(self, panier, code_promotionnel, 
                                              produit_sans_promo):
        """
        Arrange: Un panier avec coupon 20%
        Act: Calculer total avec coupon
        Assert: Réduction correcte appliquée
        """
        # Arrange
        panier.coupon = code_promotionnel
        panier.save()
        code_promotionnel.reduction = 0.20
        code_promotionnel.save()
        
        ProduitPanier.objects.create(
            produit=produit_sans_promo,
            panier=panier,
            quantite=1,
        )
        
        # Act
        total_original = panier.total
        total_with_coupon = panier.total_with_coupon
        
        # Assert
        expected_reduction = 0.20 * total_original
        expected_final = int(total_original - expected_reduction)
        assert total_with_coupon == expected_final

    @pytest.mark.unit
    def test_panier_without_coupon(self, panier, produit_sans_promo):
        """
        Arrange: Un panier sans coupon
        Act: Calculer total with coupon
        Assert: Doit être égal au total
        """
        # Arrange
        ProduitPanier.objects.create(
            produit=produit_sans_promo,
            panier=panier,
            quantite=1,
        )
        
        # Act
        total = panier.total
        total_with_coupon = panier.total_with_coupon
        
        # Assert
        assert total == total_with_coupon


class TestProduitPanierModel:
    """Tests unitaires pour le modèle ProduitPanier"""

    @pytest.mark.unit
    def test_produit_panier_creation(self, panier, produit_sans_promo):
        """
        Arrange: Un panier et un produit
        Act: Ajouter le produit au panier
        Assert: L'association doit être créée
        """
        # Arrange & Act
        pp = ProduitPanier.objects.create(
            produit=produit_sans_promo,
            panier=panier,
            quantite=1,
        )
        
        # Assert
        assert pp.id is not None
        assert pp.produit == produit_sans_promo
        assert pp.panier == panier

    @pytest.mark.unit
    def test_produit_panier_total_calculation(self, panier, produit_sans_promo):
        """
        Arrange: Un produit à 5000 avec quantité 3
        Act: Calculer le total
        Assert: Total = 5000 * 3 = 15000
        """
        # Arrange
        pp = ProduitPanier.objects.create(
            produit=produit_sans_promo,
            panier=panier,
            quantite=3,
        )
        
        # Act
        total = pp.total
        
        # Assert
        assert total == 15000

    @pytest.mark.unit
    def test_produit_panier_quantity_variations(self, panier, produit_sans_promo):
        """
        Arrange: Différentes quantités
        Act: Tester le calcul avec différentes quantités
        Assert: Total = prix * quantité
        """
        # Arrange
        test_cases = [
            (1, 5000),
            (5, 25000),
            (10, 50000),
            (100, 500000),
        ]
        
        # Act & Assert
        for qty, expected_total in test_cases:
            pp = ProduitPanier.objects.create(
                produit=produit_sans_promo,
                panier=panier,
                quantite=qty,
            )
            assert pp.total == expected_total
            pp.delete()

    @pytest.mark.unit
    def test_produit_panier_with_promo_product(self, panier, produit_avec_promo_active):
        """
        Arrange: Un produit en promotion dans un panier
        Act: Calculer le total
        Assert: Total doit utiliser le prix promo (4500 * quantité)
        """
        # Arrange
        quantite = 2
        pp = ProduitPanier.objects.create(
            produit=produit_avec_promo_active,
            panier=panier,
            quantite=quantite,
        )
        
        # Act
        total = pp.total
        
        # Assert
        expected_total = produit_avec_promo_active.prix_promotionnel * quantite
        assert total == expected_total
        assert total == 9000  # 4500 * 2
