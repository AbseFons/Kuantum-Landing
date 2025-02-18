const selectedExam = localStorage.getItem('selectedExam') || '../data/examenPrueba.json';

if (!selectedExam || !selectedExam.endsWith('.json')) {
    selectedExam = 'data/examenPrueba.json';
}

fetch(`../${selectedExam}`)
    .then(response => response.json())
    .then(data => {
        const content = data;
        const questionsArea = document.querySelector('.questions-area');

        totalQuestions = content.filter(item => item.type === "question").length;

        localStorage.setItem('examQuestions', JSON.stringify(content));

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
                        ${item.image ? `
                            <figure>
                                <img src="${item.image}" alt="Imagen relacionada con el texto" class="graphic-img">
                                ${item.caption ? `<figcaption>${item.caption}</figcaption>` : ""}
                            </figure>
                        ` : ""}
                        ${item.content_after_image ? `<p>${item.content_after_image}</p>` : ""}
                    </div>
                `;
                questionsArea.appendChild(textCard);
            } else if (item.type === "question") {
                const questionCard = document.createElement('div');
                questionCard.classList.add('question-card');
                questionCard.setAttribute('data-category', item.category);
                questionCard.innerHTML = `
                    <div class="question-header">
                        <span class="question-number">Pregunta ${item.number}</span>
                        <span class="question-category">${item.category}</span>
                    </div>
                    <div class="question-body">
                        <p class="question-text">${item.text}</p>
                        ${item.image ? `
                            <figure>
                                <img src="${item.image}" alt="Imagen de la pregunta ${item.number}" class="question-img">
                            </figure>
                        ` : ""}
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

        attachProgressEvent();
        attachFilterEvent();
        attachFinishEvent();

        document.querySelectorAll('.question-options input[type="radio"]').forEach((input) => {
            input.addEventListener('change', (e) => {
                const questionNumber = e.target.name.replace('question', '');
                const selectedAnswer = e.target.value;

                let userAnswers = JSON.parse(localStorage.getItem('userAnswers')) || {};
                userAnswers[questionNumber] = selectedAnswer;
                localStorage.setItem('userAnswers', JSON.stringify(userAnswers));
            });
        });

        updateProgress();
        filterContent('all');
    })
    .catch(error => console.error('Error cargando el JSON:', error));

document.querySelectorAll('.report-link').forEach((link) => {
    link.addEventListener('click', (e) => {
        e.preventDefault();

        const questionNumber = e.target.dataset.questionNumber;
        console.log('Número de la pregunta:', questionNumber);  // Verificar el número

        document.getElementById('reportForm').dataset.questionNumber = questionNumber;

        showReportModal();
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const nombreAlumno = localStorage.getItem("nombreAlumno") || "Estudiante";
    document.getElementById("student-name").textContent = nombreAlumno;

    const selectedExam = localStorage.getItem("selectedExam");

    let examNumber = "1"; // Valor por defecto
    if (selectedExam.includes("examenPrueba2.json")) {
        examNumber = "2";
    } else if (selectedExam.includes("examenPrueba3.json")) {
        examNumber = "3";
    }

    document.getElementById("exam-title").textContent = `Examen Beca 18 N° ${examNumber}`;
});

// Función para mostrar el modal Reporte
function showReportModal() {
    const reportModal = document.getElementById('reportModal');
    if (reportModal) {
        reportModal.style.display = 'flex';
    } else {
        console.error('Modal de reporte no encontrado.');
    }
}

function hideReportModal() {
    const reportModal = document.getElementById('reportModal');
    if (reportModal) {
        reportModal.style.display = 'none';
    }
}

const cancelReportButton = document.getElementById('cancelReport');
if (cancelReportButton) {
    cancelReportButton.addEventListener('click', hideReportModal);
}

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
let totalQuestions = 0;
let answeredQuestions = 0;

function updateProgress() {
    answeredQuestions = document.querySelectorAll('.question-options input[type="radio"]:checked').length;
    const progressPercentage = (answeredQuestions / totalQuestions) * 100;

    document.querySelector('.progress').style.width = `${progressPercentage}%`;
    document.querySelector('.progress-section p').textContent = `${answeredQuestions} de ${totalQuestions} preguntas resueltas`;
}

function attachProgressEvent() {
    document.querySelectorAll('.question-options input[type="radio"]').forEach(input => {
        input.addEventListener('change', updateProgress);
    });
}

// Temporizador
let totalTimeInMinutes = 120; //Minutos del examen
let remainingTimeInSeconds = totalTimeInMinutes * 60;
let timerStopped = false; 

function showTimeUpModal() {
    const modal = document.getElementById('timeUpModal');
    if (modal) {
        modal.style.display = 'flex';
    }
    document.querySelector('.timer').textContent = "00:00:00";
    timerStopped = true;
}

function goToResults() {
    window.location.href = "reporte.html"; 
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

// Filtrado de Preguntas
function attachFilterEvent() {
    document.querySelectorAll('input[name="course-filter"]').forEach((radio) => {
        radio.addEventListener('change', () => {
            const selectedCategory = document.querySelector('input[name="course-filter"]:checked').value;
            filterContent(selectedCategory);
        });
    });
}

function filterContent(category) {
    const allCards = document.querySelectorAll('.question-card, .text-card');

    allCards.forEach((card) => {
        const cardCategory = card.getAttribute('data-category');
        card.style.display = (category === 'all' || cardCategory === category) ? 'block' : 'none';
    });
}

attachFilterEvent();
filterContent('all');


// Finalización del Examen
function attachFinishEvent() {
    let userAnswers = JSON.parse(localStorage.getItem('userAnswers')) || {};

    const confirmationModal = document.getElementById("confirmationModal");
    const timeUpModal = document.getElementById("timeUpModal");
    const remainingTimeElement = document.getElementById("remaining-time");
    const unansweredQuestionsElement = document.getElementById("unanswered-questions");
    const confirmFinishButton = document.getElementById("confirmFinish");
    const cancelFinishButton = document.getElementById("cancelFinish");

    const finishButton = document.querySelector(".btn-finish");

    finishButton.addEventListener("click", showConfirmationModal);
    confirmFinishButton.addEventListener("click", confirmFinish);
    cancelFinishButton.addEventListener("click", hideConfirmationModal);

    document.querySelectorAll('.question-options input[type="radio"]').forEach((input) => {
        input.addEventListener('change', (e) => {
            const questionNumber = e.target.name.replace('question', '');
            userAnswers[questionNumber] = e.target.value;
            localStorage.setItem('userAnswers', JSON.stringify(userAnswers));
        });
    });

    function showConfirmationModal() {
        updateConfirmationTime();
        confirmationTimerInterval = setInterval(updateConfirmationTime, 1000);

        const unansweredQuestions = totalQuestions - Object.keys(userAnswers).length;
        unansweredQuestionsElement.textContent = unansweredQuestions;

        confirmationModal.style.display = "flex";
    }

    function hideConfirmationModal() {
        confirmationModal.style.display = "none";
        clearInterval(confirmationTimerInterval);
    }

    function updateConfirmationTime() {
        const minutes = Math.floor(remainingTimeInSeconds / 60);
        const seconds = remainingTimeInSeconds % 60;
        const formattedTime = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
        remainingTimeElement.textContent = formattedTime;
    }

    function confirmFinish() {
        hideConfirmationModal();
        showTimeUpModal(); 
    }
}


const header = document.querySelector('.header');
const sidebar = document.querySelector('.sidebar');

// Inicializamos la posición del sidebar al cargar la página
let initialTopPosition = header.offsetHeight;

sidebar.style.top = `${initialTopPosition}px`;

function handleScroll() {
    const scrollPosition = window.scrollY;
    const headerHeight = header.offsetHeight; 

    if (scrollPosition > headerHeight) {
        sidebar.style.top = "0"; 
    } else {
        sidebar.style.top = `${headerHeight - scrollPosition}px`; 
    }
}

window.addEventListener('scroll', handleScroll);

document.addEventListener("DOMContentLoaded", function() {
    const logoLink = document.getElementById("logo-link");
    const modal = document.getElementById("modal-confirmation");
    const confirmBtn = document.getElementById("confirm-return");
    const cancelBtn = document.getElementById("cancel-return");

    logoLink.addEventListener("click", function(event) {
        event.preventDefault(); 
        modal.style.display = "flex"; 
    });

    confirmBtn.addEventListener("click", function() {
        window.location.href = "../index.html"; 
    });

    cancelBtn.addEventListener("click", function() {
        modal.style.display = "none";
    });
});

