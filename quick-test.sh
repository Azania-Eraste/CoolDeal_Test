#!/bin/bash
# quick-test.sh - Commandes rapides pour tester le projet CoolDeal

echo "🧪 CoolDeal - Commandes Tests Rapides"
echo "====================================="
echo ""

# Couleurs pour l'output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Installation des dépendances:${NC}"
echo "   pip install -r requirements-test.txt"
echo ""

echo -e "${BLUE}2. Exécuter TOUS les tests:${NC}"
echo "   pytest"
echo ""

echo -e "${BLUE}3. Tests UNITAIRES uniquement:${NC}"
echo "   pytest -m unit"
echo ""

echo -e "${BLUE}4. Tests INTÉGRATION uniquement:${NC}"
echo "   pytest -m integration"
echo ""

echo -e "${BLUE}5. Tests d'une app spécifique:${NC}"
echo "   pytest shop/tests/"
echo "   pytest customer/tests/"
echo ""

echo -e "${BLUE}6. Rapport de couverture (HTML):${NC}"
echo "   pytest --cov=. --cov-exclude=*/migrations/* --cov-exclude=*/venv/* --cov-report=html --cov-report=term-missing"
echo "   # Puis ouvrir: htmlcov/index.html"
echo ""

echo -e "${BLUE}7. Tests avec output détaillé:${NC}"
echo "   pytest -v       # Verbose"
echo "   pytest -s       # Afficher les print()"
echo "   pytest -vv      # Très détaillé"
echo ""

echo -e "${BLUE}8. Tests les plus lents:${NC}"
echo "   pytest --durations=10"
echo ""

echo -e "${BLUE}9. Réexécuter tests échoués:${NC}"
echo "   pytest --lf"
echo ""

echo -e "${BLUE}10. Tests en parallèle (plus rapide):${NC}"
echo "    pytest -n auto"
echo ""

echo -e "${YELLOW}💡 TIP: Consulter TESTING_GUIDE.py pour plus d'options${NC}"
