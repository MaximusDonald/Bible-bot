// Fonction pour injecter du CSS dynamiquement
function addCustomCSS() {
    const styleElement = document.createElement('style');
    styleElement.textContent = `
      a img[alt="watermark"] {
        display: none;
      }
    `;
    document.head.appendChild(styleElement);
  }
  
  
  function loadGoogleFonts() {
      const fontLink = document.createElement("link");
      fontLink.href = "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&family=Tagesschrift&display=swap";
      fontLink.rel = "stylesheet";
      document.head.appendChild(fontLink);
      
  }
  
  // Fonction pour modifier le lien Chainlit
  function changeChainlitLink() {
      loadGoogleFonts();
  
      // Sélectionner tous les liens qui contiennent l'URL de Chainlit
      const chainlitLinks = document.querySelectorAll('a[href*="chainlit.io"], a[href*="github.com/Chainlit/chainlit"]');
  
      chainlitLinks.forEach(link => {
          // Changer l'URL du lien
          link.href = "https://github.com/Ghilth/";
  
          // Changer le texte du lien
          link.textContent = "Made by Ghilth GBAGUIDI";
  
          // Changer la police
          link.style.fontFamily = "'Tagesschrift', sans-serif";  // Utiliser une police Google Fonts
  
          // Rendre le lien visible s'il était caché
          link.style.visibility = "visible";
      });
  }
  
  
  
  // Exécuter les fonctions lorsque le DOM est chargé
  document.addEventListener('DOMContentLoaded', () => {
    addCustomCSS();
    changeChainlitLink();
  });
  
  // Si les éléments sont chargés dynamiquement après le chargement de la page
  // vous pourriez avoir besoin d'un MutationObserver
  const observer = new MutationObserver((mutations) => {
    addCustomCSS();
    changeChainlitLink();
  });
  
  // Commencer à observer le document avec la configuration définie
  observer.observe(document.body, { 
    childList: true,
    subtree: true 
  });