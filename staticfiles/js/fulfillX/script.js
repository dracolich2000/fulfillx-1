// Smooth Scrolling
document.querySelectorAll('nav ul li a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({ behavior: 'smooth' });
    });
  });
  
  // Submit Form
  document.querySelector('form').addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Message sent successfully!');
  });