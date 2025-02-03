const selectedExam = localStorage.getItem('selectedExam') || '../data/examenPrueba.json';

if (!selectedExam || !selectedExam.endsWith('.json')) {
    selectedExam = 'data/examenPrueba.json';
}

fetch(`../${selectedExam}`)
    .then(response => response.json())
    .then(data => {
        const content = data;
        const questionsArea = document.querySelector('.questions-area');

        content.forEach((item) => {
            if (item.type === "text-card") {
                const textCard = document.createElement('div');
                textCard.classList.add('text-card');
                textCard.setAttribute('data-category', item.category);
                textCard.innerHTML = `
                    <div class="text-header">
                        <span class="text-title">${item.title}:</span>
                        <span class="text-label">${item.label}</span>
                    </div>
                    <div class="text-body">
                        <p>${item.content}</p>
                        ${
                            item.image
                                ? `
                                    <figure>
                                        <img src="${item.image}" alt="Imagen relacionada con el texto" class="graphic-img">
                                        ${item.caption ? `<figcaption>${item.caption}</figcaption>` : ""}
                                    </figure>
                                `
                                : ""
                        }
                    </div>
                `;
                questionsArea.appendChild(textCard);
            } else if (item.type === "question") {
                const questionCard = document.createElement('div');
                questionCard.classList.add('question-card');
                questionCard.innerHTML = `
                    <div class="question-header">
                        <span class="question-number">Pregunta ${item.number}</span>
                        <span class="question-category">${item.category}</span>
                    </div>
                    <div class="question-body">
                        <p class="question-text">${item.text}</p>
                        
                        <!-- Agregar la imagen si existe -->
                        ${item.image ? `
                            <figure>
                                <img src="${item.image}" alt="Imagen de la pregunta ${item.number}" class="question-img">
                            </figure>
                        ` : ''}
            
                        <div class="question-options">
                            ${item.options.map((option, index) => `
                                <label>
                                    <input type="radio" name="question${item.number}" value="${String.fromCharCode(65 + index)}">
                                    ${String.fromCharCode(65 + index)}. ${option}
                                </label>
                            `).join('')}
                        </div>
                    </div>
                    <div class="question-footer">
                        <a href="#" class="report-link" data-question-number="${item.number}">Reportar pregunta</a>
                    </div>
                `;
                questionsArea.appendChild(questionCard);
            }            
        });

        document.querySelectorAll('.report-link').forEach((link) => {
            link.addEventListener('click', (e) => {
                e.preventDefault();

                const questionNumber = e.target.dataset.questionNumber;

                document.getElementById('reportForm').dataset.questionNumber = questionNumber;
                showReportModal();
            });
        });
}).catch(error => console.error('Error cargando el JSON:', error));



// Seleccionar todos los enlaces "Reportar pregunta"
document.querySelectorAll('.report-link').forEach((link) => {
    link.addEventListener('click', (e) => {
        e.preventDefault();

        // Obtener el número de la pregunta directamente desde el atributo data
        const questionNumber = e.target.dataset.questionNumber;
        console.log('Número de la pregunta:', questionNumber);  // Verificar el número

        // Guardar el número de la pregunta en el formulario del modal
        document.getElementById('reportForm').dataset.questionNumber = questionNumber;

        showReportModal();
    });
});


// Función para mostrar el modal
function showReportModal() {
    const reportModal = document.getElementById('reportModal');
    if (reportModal) {
        reportModal.style.display = 'flex';
    } else {
        console.error('Modal de reporte no encontrado.');
    }
}

// Función para ocultar el modal
function hideReportModal() {
    const reportModal = document.getElementById('reportModal');
    if (reportModal) {
        reportModal.style.display = 'none';
    }
}

// Evento para cerrar el modal con el botón de cancelar
const cancelReportButton = document.getElementById('cancelReport');
if (cancelReportButton) {
    cancelReportButton.addEventListener('click', hideReportModal);
}

// Enviar reporte
const submitReportButton = document.getElementById('submitReport');
if (submitReportButton) {
    submitReportButton.addEventListener('click', () => {
        const reportForm = document.getElementById('reportForm');
        const reason = document.querySelector('input[name="report-reason"]:checked')?.value;
        const details = document.getElementById('report-details').value;
        const questionNumber = reportForm.dataset.questionNumber;

        if (reason) {
            const reportData = {
                questionNumber,
                reason,
                details
            };

            console.log('Reporte enviado:', reportData);

            // Aquí podrías enviar los datos a un servidor o guardarlos localmente
            // Ejemplo de almacenamiento local:
            let reports = JSON.parse(localStorage.getItem('reports')) || [];
            reports.push(reportData);
            localStorage.setItem('reports', JSON.stringify(reports));

            hideReportModal();
            alert(`Reporte de la Pregunta ${questionNumber} enviado exitosamente.`);
        } else {
            alert('Por favor selecciona un motivo para el reporte.');
        }
    });
}


// Barra de Progreso
const totalQuestions = content.filter(item => item.type === "question").length;
let answeredQuestions = 0;

function updateProgress() {
    answeredQuestions = document.querySelectorAll('.question-options input[type="radio"]:checked').length;
    const progressPercentage = (answeredQuestions / totalQuestions) * 100;

    document.querySelector('.progress').style.width = `${progressPercentage}%`;
    document.querySelector('.progress-section p').textContent = `${answeredQuestions} de ${totalQuestions} preguntas resueltas`;
}

document.querySelectorAll('.question-options input[type="radio"]').forEach(input => {
    input.addEventListener('change', updateProgress);
});

updateProgress();

// Variable global para temporizador
let totalTimeInMinutes = 10; 
let remainingTimeInSeconds = totalTimeInMinutes * 60;

let timerStopped = false; 

function showTimeUpModal() {
    const modal = document.getElementById('timeUpModal');
    modal.style.display = 'flex';
    document.querySelector('.timer').textContent = "00:00:00";
    timerStopped = true;
}

function goToResults() {
    window.location.href = "resultados.html"; 
}

function updateTimer() {
    if (timerStopped) return; 

    if (remainingTimeInSeconds <= 0) {
        remainingTimeInSeconds = 0; 
        clearInterval(timerInterval); 
        showTimeUpModal(); 
        return;
    }

    const hours = Math.floor(remainingTimeInSeconds / 3600);
    const minutes = Math.floor((remainingTimeInSeconds % 3600) / 60);
    const seconds = remainingTimeInSeconds % 60;

    const formattedTime = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    document.querySelector('.timer').textContent = formattedTime;

    remainingTimeInSeconds--; 
}

const timerInterval = setInterval(updateTimer, 1000);
updateTimer();



document.querySelectorAll('input[name="course-filter"]').forEach((radio) => {
    radio.addEventListener('change', () => {
        const selectedCategory = document.querySelector('input[name="course-filter"]:checked').value;
        filterContent(selectedCategory);
    });
});

function filterContent(category) {
    const questionCards = document.querySelectorAll('.question-card');
    const textCards = document.querySelectorAll('.text-card');

    questionCards.forEach((card) => {
        const cardCategory = card.querySelector('.question-category').textContent.trim();
        card.style.display = category === 'all' || cardCategory === category ? 'block' : 'none';
    });

    textCards.forEach((card) => {
        const cardCategory = card.getAttribute('data-category');
        card.style.display = category === 'all' || cardCategory === category ? 'block' : 'none';
    });
}

filterContent('all');


let userAnswers = JSON.parse(localStorage.getItem('userAnswers')) || {};

const confirmationModal = document.getElementById("confirmationModal");
const timeUpModal = document.getElementById("timeUpModal");
const remainingTimeElement = document.getElementById("remaining-time");
const unansweredQuestionsElement = document.getElementById("unanswered-questions");
const confirmFinishButton = document.getElementById("confirmFinish");
const cancelFinishButton = document.getElementById("cancelFinish");

const finishButton = document.querySelector(".btn-finish");

function showConfirmationModal() {
    const minutes = Math.floor(remainingTimeInSeconds / 60);
    const seconds = remainingTimeInSeconds % 60;
    const formattedTime = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    remainingTimeElement.textContent = formattedTime;

    const unansweredQuestions = totalQuestions - Object.keys(userAnswers).length;
    unansweredQuestionsElement.textContent = unansweredQuestions;

    confirmationModal.style.display = "flex";
}

function hideConfirmationModal() {
    confirmationModal.style.display = "none";
}

function confirmFinish() {
    hideConfirmationModal();
    showTimeUpModal(); 
}

finishButton.addEventListener("click", showConfirmationModal);
confirmFinishButton.addEventListener("click", confirmFinish);
cancelFinishButton.addEventListener("click", hideConfirmationModal);

document.querySelectorAll('.question-options input[type="radio"]').forEach((input) => {
    input.addEventListener('change', (e) => {
        const questionNumber = e.target.name.replace('question', ''); // Obtener el número de la pregunta
        userAnswers[questionNumber] = e.target.value; // Guardar respuesta seleccionada
        localStorage.setItem('userAnswers', JSON.stringify(userAnswers)); // Guardar en localStorage
    });
});



const header = document.querySelector('.header');
const sidebar = document.querySelector('.sidebar');

// Inicializamos la posición del sidebar al cargar la página
let initialTopPosition = header.offsetHeight;

// Configuramos el estilo inicial del sidebar
sidebar.style.top = `${initialTopPosition}px`;

// Función para manejar el desplazamiento del usuario
function handleScroll() {
    const scrollPosition = window.scrollY; // Posición del scroll vertical
    const headerHeight = header.offsetHeight; // Altura del header

    if (scrollPosition > headerHeight) {
        sidebar.style.top = "0"; // Fija el sidebar al tope de la ventana
    } else {
        sidebar.style.top = `${headerHeight - scrollPosition}px`; // Ajusta dinámicamente
    }
}

// Agrega el Event Listener para el evento scroll
window.addEventListener('scroll', handleScroll);

document.addEventListener("DOMContentLoaded", function() {
    const logoLink = document.getElementById("logo-link");
    const modal = document.getElementById("modal-confirmation");
    const confirmBtn = document.getElementById("confirm-return");
    const cancelBtn = document.getElementById("cancel-return");

    // Evita la redirección inmediata y muestra el modal
    logoLink.addEventListener("click", function(event) {
        event.preventDefault(); // Evita que el enlace funcione de inmediato
        modal.style.display = "flex"; // Muestra el modal
    });

    // Si el usuario confirma, redirigir a index.html
    confirmBtn.addEventListener("click", function() {
        window.location.href = "../index.html"; // Redirige
    });

    // Si el usuario cancela, ocultar el modal
    cancelBtn.addEventListener("click", function() {
        modal.style.display = "none";
    });
});

