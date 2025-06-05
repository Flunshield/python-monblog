// Script de débogage pour le générateur Gemini
// À coller dans la console du navigateur

console.log("🔍 Démarrage du débogage Gemini...");

// Vérifier que les éléments existent
const form = document.getElementById('gemini-form');
const generateBtn = document.getElementById('generate-btn');
const promptField = document.getElementById('prompt');

console.log("📋 Éléments trouvés:");
console.log("Form:", form);
console.log("Button:", generateBtn);
console.log("Prompt field:", promptField);

// Vérifier si le formulaire a un event listener
if (form) {
    console.log("✅ Formulaire trouvé");
    
    // Ajouter un test d'envoi manuel
    window.testGeminiSubmit = function() {
        console.log("🧪 Test d'envoi manuel...");
        
        const prompt = promptField.value.trim() || "Test article sur les chats";
        const language = "fr";
        
        console.log("📝 Données:", { prompt, language });
        
        const formData = {
            resume: prompt,
            langue: language
        };
        
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        console.log("🔐 CSRF Token:", csrfToken ? csrfToken.substring(0, 10) + "..." : "NON TROUVÉ");
        
        fetch('/generate-article-ai/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            console.log("📡 Réponse:", response.status, response.statusText);
            return response.text();
        })
        .then(data => {
            console.log("📦 Données reçues:", data);
            try {
                const parsed = JSON.parse(data);
                console.log("✅ JSON parsé:", parsed);
            } catch (e) {
                console.log("❌ Pas du JSON valide");
            }
        })
        .catch(error => {
            console.error("❌ Erreur:", error);
        });
    };
    
    console.log("🎯 Utilisez testGeminiSubmit() pour tester manuellement");
    
    // Vérifier l'event listener sur le formulaire
    const events = getEventListeners ? getEventListeners(form) : "getEventListeners non disponible";
    console.log("🎧 Event listeners:", events);
    
} else {
    console.log("❌ Formulaire non trouvé !");
}

// Tester le bouton
if (generateBtn) {
    console.log("✅ Bouton trouvé, état:", generateBtn.disabled ? "désactivé" : "activé");
} else {
    console.log("❌ Bouton non trouvé !");
}

console.log("🔍 Fin du débogage initial. Tapez testGeminiSubmit() pour tester.");
