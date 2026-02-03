"""
GUIDE DE TESTS AUTOMATISÉS - COOLDEAL PROJECT
==============================================

Ce guide vous explique comment configurer et exécuter les tests pour le projet CoolDeal.
"""

# ============================================================================
# 1. INSTALLATION DES DÉPENDANCES DE TEST
# ============================================================================

"""
Installez les packages nécessaires pour les tests:

    pip install pytest pytest-django pytest-cov pytest-mock coverage

Détails des packages:
- pytest: Framework de test
- pytest-django: Intégration Django avec pytest
- pytest-cov: Plugin pour la couverture de code (coverage)
- pytest-mock: Helpers pour les mocks
- coverage: Rapport de couverture de code détaillé
"""


# ============================================================================
# 2. COMMANDES POUR EXÉCUTER LES TESTS
# ============================================================================

"""
Exécuter TOUS les tests:
    pytest

Exécuter les tests d'une application spécifique:
    pytest shop/tests/
    pytest customer/tests/
    pytest contact/tests/

Exécuter UNIQUEMENT les tests unitaires:
    pytest -m unit

Exécuter UNIQUEMENT les tests d'intégration:
    pytest -m integration

Exécuter un fichier de test spécifique:
    pytest shop/tests/test_models.py
    pytest customer/tests/test_authentication.py

Exécuter un test/classe spécifique:
    pytest shop/tests/test_models.py::TestProduitPrixLogic
    pytest shop/tests/test_models.py::TestProduitPrixLogic::test_produit_prix_sans_promotion

Exécuter avec affichage détaillé (verbose):
    pytest -v
    pytest -vv  (encore plus détaillé)

Exécuter avec affichage des print statements:
    pytest -s

Exécuter avec affichage du temps d'exécution:
    pytest --durations=10
"""


# ============================================================================
# 3. COMMANDES POUR LA COUVERTURE (COVERAGE)
# ============================================================================

"""
Générer un rapport de couverture (HTML + Terminal):
    pytest --cov=. --cov-exclude=*/migrations/* --cov-exclude=*/venv/* --cov-report=html --cov-report=term-missing

Générer rapport de couverture avec détails:
    coverage run -m pytest
    coverage report -m

Générer rapport HTML de couverture:
    coverage html
    # Ouvrir htmlcov/index.html dans le navigateur

Afficher couverture pour une app spécifique:
    pytest --cov=shop shop/tests/
    pytest --cov=customer customer/tests/

Exclure des fichiers/dossiers du rapport:
    pytest --cov=. --cov-exclude=*/migrations/* --cov-exclude=*/venv/* --cov-exclude=*/tests/*
"""


# ============================================================================
# 4. EXÉCUTION DES TESTS AVEC PYTEST.INI
# ============================================================================

"""
Le fichier pytest.ini à la racine du projet configure automatiquement:
- DJANGO_SETTINGS_MODULE = cooldeal.settings
- Patterns de découverte des tests
- Rapports de couverture
- Marqueurs personnalisés

Vous n'avez donc que besoin de:
    pytest

Et tout est configuré automatiquement!
"""


# ============================================================================
# 5. STRUCTURE DES TESTS
# ============================================================================

"""
Les tests sont organisés comme suit:

├── pytest.ini (Configuration générale)
├── conftest.py (Fixtures réutilisables)
├── shop/
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py (Tests unitaires des modèles)
│       └── test_payments.py (Tests d'intégration paiement)
├── customer/
│   └── tests/
│       ├── __init__.py
│       ├── test_authentication.py (Tests d'intégration login)
│       └── test_models.py (Tests unitaires)
├── contact/tests/
└── client/tests/

Structure AAA respectée dans chaque test:
  - Arrange: Préparation des données de test
  - Act: Exécution du code à tester
  - Assert: Vérification des résultats
"""


# ============================================================================
# 6. FIXTURES DISPONIBLES
# ============================================================================

"""
Les fixtures pytest sont définies dans conftest.py et disponibles partout:

UTILISATEURS:
- user(db): Crée un utilisateur de test
- another_user(db): Crée un second utilisateur
- user_data: Dictionnaire de données utilisateur

GÉOLOCALISATION:
- city(db): Retourne/crée une ville

SHOP:
- categorie_etablissement(db): Catégorie d'établissement
- categorie_produit(db, categorie_etablissement): Catégorie de produit
- etablissement(db, user, categorie_etablissement, city): Vendeur
- produit_sans_promo(db, ...): Produit SANS promotion
- produit_avec_promo_active(db, ...): Produit EN promotion
- produit_avec_promo_expirée(db, ...): Produit AVEC promo EXPIRÉE
- produit_super_deal(db, ...): Super deal vedette

CUSTOMER:
- customer(db, user, city): Profil client
- code_promotionnel(db, produit_sans_promo): Code de réduction
- panier(db, customer): Panier vide
- produit_panier(db, panier, produit_sans_promo): Produit dans panier
- commande(db, customer): Commande
- password_reset_token(db, user): Token réinitialisation

CONTACT:
- contact_message(db): Message de contact
- newsletter_subscriber(db): Abonné newsletter

UTILITIES:
- favorite(db, user, produit_sans_promo): Produit favori
- api_client(): Client API pour tests
"""


# ============================================================================
# 7. MOCKS POUR LES APPELS EXTERNES
# ============================================================================

"""
Le projet utilise unittest.mock pour simuler les appels API externes:

Exemple - Mock CinetPay:
    @patch('cinetpay_sdk.s_d_k.Cinetpay')
    def test_payment(self, mock_cinetpay):
        mock_instance = MagicMock()
        mock_cinetpay.return_value = mock_instance
        mock_instance.generate_payment_url.return_value = {...}
        
        # Test votre code...

Les tests utilisent @patch et MagicMock pour éviter:
- Appels réels aux services de paiement
- Dépendances externes
- Ralentissement des tests
"""


# ============================================================================
# 8. MARQUEURS PERSONNALISÉS
# ============================================================================

"""
Deux marqueurs sont disponibles dans pytest.ini:

@pytest.mark.unit
- Tests unitaires rapides
- Testent une fonction/méthode isolée
- Pas d'accès à la BD sauf fixture db

@pytest.mark.integration  
- Tests d'intégration
- Testent plusieurs composants ensemble
- Exemple: flux complet login → créer profil

Utilisation:
    pytest -m unit      # Uniquement unitaires
    pytest -m integration  # Uniquement intégration
    pytest -m "not slow"   # Exclure les lents
"""


# ============================================================================
# 9. BONNES PRATIQUES DE TEST
# ============================================================================

"""
✅ À FAIRE:
1. Respecter la structure AAA (Arrange, Act, Assert)
2. Un test = une responsabilité
3. Utiliser les fixtures pytest plutôt que setUp()
4. Mocker les appels externes (API, emails, etc.)
5. Tester les cas normaux ET les cas d'erreur
6. Nommer explicitement: test_<fonction>_<cas>_<résultat>
7. Utiliser les marqueurs @pytest.mark.unit/integration

❌ À ÉVITER:
1. Ne pas tester l'implémentation, tester le comportement
2. Ne pas créer d'état global (utiliser fixtures)
3. Éviter les tests qui dépendent les uns des autres
4. Ne pas faire d'assertions multiples sans logique
5. Ne pas oublier le (db) fixture si besoin d'accès BD
"""


# ============================================================================
# 10. EXEMPLES DE COMMANDES PRATIQUES
# ============================================================================

"""
# Exécuter et arrêter au premier échec
pytest -x

# Arrêter après 3 échouages
pytest --maxfail=3

# Réexécuter uniquement les tests échoués
pytest --lf

# Exécuter tests et afficher les plus lents
pytest --durations=5

# Générer rapport HTML + Terminal avec coverage
pytest --cov=. --cov-exclude=*/migrations/* --cov-report=html --cov-report=term-missing

# Exécuter tests avec logs de Django
pytest --log-cli-level=DEBUG

# Paralléliser les tests (plus rapide)
pip install pytest-xdist
pytest -n auto

# Watch mode (réexécute au changement de fichier)
pip install pytest-watch
ptw
"""


# ============================================================================
# 11. CONFIGURATION POUR CI/CD (GitHub Actions, GitLab CI, etc.)
# ============================================================================

"""
Exemple de commande pour une pipeline CI:
    pytest --cov=. \\
           --cov-exclude=*/migrations/* \\
           --cov-exclude=*/venv/* \\
           --cov-report=term-missing \\
           --cov-report=xml \\
           -v

Cela:
- Lance tous les tests
- Génère un rapport de couverture détaillé
- Affiche les résultats en verbose
- Crée un fichier coverage.xml pour les intégrations
"""


# ============================================================================
# 12. RÉSOLUTION DE PROBLÈMES COURANTS
# ============================================================================

"""
Erreur: "ModuleNotFoundError: No module named 'pytest_django'"
Solução: pip install pytest-django

Erreur: "DJANGO_SETTINGS_MODULE not set"
Solution: Vérifiez que pytest.ini existe à la racine avec DJANGO_SETTINGS_MODULE

Erreur: "Database 'default' does not exist"
Solution: pytest crée automatiquement une BD test, vérifiez les migrations:
    python manage.py migrate

Erreur: "django.core.exceptions.ImproperlyConfigured"
Solution: Vérifiez cooldeal/settings.py est accessible et valide

Tests lents?
Solution: Utilisez --durations=10 pour identifier les goulots
          Utilisez pytest -n auto pour paralléliser
          Moquez les requêtes externes
"""
