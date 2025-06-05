// Script de débogage pour le générateur Gemini
console.log('🔧 Script de débogage chargé');

// Vérifier que tous les éléments sont présents
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM Ready');
    
    // Vérifier les éléments critiques
    const elements = {
        form: document.getElementById('gemini-form'),
        generateBtn: document.getElementById('generate-btn'),
        promptField: document.getElementById('prompt'),
        languageField: document.getElementById('language'),
        csrfToken: document.querySelector('[name=csrfmiddlewaretoken]')
    };
    
    console.log('🔍 Éléments trouvés:');
    Object.keys(elements).forEach(key => {
        if (elements[key]) {
            console.log(`✅ ${key}: OK`);
        } else {
            console.log(`❌ ${key}: MANQUANT`);
        }
    });
    
    // Test d'événement sur le formulaire
    if (elements.form) {
        console.log('📝 Ajout de l\'event listener sur le formulaire');
        elements.form.addEventListener('submit', function(e) {
            console.log('🚀 ÉVÉNEMENT SUBMIT DÉCLENCHÉ !');
            e.preventDefault();
            alert('Le JavaScript fonctionne ! L\'événement submit est capturé.');
        });
    }
    
    // Test sur le bouton directement
    if (elements.generateBtn) {
        elements.generateBtn.addEventListener('click', function(e) {
            console.log('🖱️ BOUTON CLIQUÉ !');
        });
    }
    
    // Vérifier les URLs Django
    try {
        // Ici on teste si les templates Django sont bien interprétés
        console.log('🌐 Test des URLs Django...');
        // Note: dans un vrai template, ça donnerait l'URL réelle
    } catch (error) {
        console.error('❌ Erreur avec les templates Django:', error);
    }
});

// Fonction pour tester manuellement
window.testSubmit = function() {
    console.log('🧪 Test manuel de soumission');
    const form = document.getElementById('gemini-form');
    if (form) {
        const event = new Event('submit', { bubbles: true, cancelable: true });
        form.dispatchEvent(event);
    }
};

console.log('💡 Pour tester manuellement, tapez: testSubmit()');
