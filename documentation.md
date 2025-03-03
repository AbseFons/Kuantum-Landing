# Documentación del Proyecto: Kuantum Plataforma Web

## 1️⃣ Introducción

### 1.1. Objetivo del Documento
Este documento tiene como propósito describir las funcionalidades de la plataforma web de **Kuantum**. Está dirigido principalmente al equipo de trabajo, incluyendo administradores y futuros desarrolladores o diseñadores que necesiten comprender el sistema sin un conocimiento profundo de código. Se explicarán las funcionalidades clave, la estructura de la plataforma y su integración con tecnologías como Firestore.

### 1.2. Descripción del Proyecto
La **plataforma web Kuantum** es un sistema desarrollado para optimizar los servicios que Kuantum brindaba anteriormente a través de **Google Forms y reportes manuales**. Kuantum se enfoca en ayudar a jóvenes peruanos que postulan a **Beca 18**, proporcionándoles **simulacros de exámenes** que les permitan prepararse adecuadamente.

El sistema permite:

- **Registro de usuarios** a través de formularios, almacenando su información para contacto posterior.
- **Realización de simulacros de exámenes en línea**, con preguntas cargadas desde archivos JSON.
- **Generación automática de reportes de desempeño**, donde los resultados se almacenan en Firestore y se presentan de manera visual con gráficos.
- **Manejo de reclamaciones** a través de un libro de reclamaciones virtual.
- **Redirección a redes sociales y contacto con la administración**.

### 1.3. Público Objetivo
El sistema está diseñado para **estudiantes residentes en Perú** que postulan a **Beca 18**. Se espera que los usuarios interactúen con la plataforma ingresando sus datos, completando el simulacro y revisando sus resultados.

### 1.4. Alcance del Proyecto
La plataforma cuenta con las siguientes páginas y funcionalidades principales:

- **`index.html`** → Página principal con información sobre Kuantum y acceso al simulacro.
- **`test.html`** → Simulacro de examen cargado dinámicamente desde archivos JSON.
- **`reporte.html`** → Generación y visualización de reportes de desempeño.
- **`reclamos.html`** → Formulario virtual para registrar reclamaciones.
- **`login.html`** → Página en desarrollo sin funcionalidad implementada.

### 1.5. Funcionalidades Implementadas
Las principales funcionalidades desarrolladas hasta el momento incluyen:

- **Simulacro interactivo**: Preguntas extraídas desde JSON, con opciones de imágenes y texto.
- **Almacenamiento de respuestas en `localStorage`** y generación de reportes.
- **Automatización de reportes con cálculos y gráficos dinámicos.**
- **Envío de datos de usuarios y resultados a Firestore.**
- **Libro de Reclamaciones virtual con formulario estructurado.**

### 1.6. Funcionalidades Futuras
Aunque la plataforma ya es operativa, hay planes de expansión hacia un **LMS (Learning Management System)** con funcionalidades adicionales como:

- **Integración de autenticación (login y registro de usuarios).**
- **Implementación de una pasarela de pagos.**
- **Acceso a cursos dentro de la plataforma.**

### 1.7. Enfoque de la Documentación
Esta documentación **se centrará en explicar las funcionalidades actuales**, sin incluir instrucciones de instalación o despliegue. Su objetivo es proporcionar una visión clara del sistema a los miembros del equipo y facilitar su comprensión por parte de futuros colaboradores.

---

## 2️⃣ Tecnologías Utilizadas

### 2.1. Frontend
La plataforma ha sido desarrollada utilizando **HTML, CSS y JavaScript**, sin el uso de frameworks.

#### Lenguajes y Herramientas Usadas:
- **HTML5** → Estructura del contenido de la página.
- **CSS3** → Diseño y estilos personalizados sin frameworks externos.
- **JavaScript (Vanilla JS)** → Implementación de la lógica interactiva en la plataforma.

#### Fuentes y Tipografía Usadas:
- **Google Fonts** (`Josefin Sans`, `Lato`) para una apariencia estilizada.
- **Lemon Milk Font** desde `fonts.cdnfonts.com`.

#### Elementos Clave de la Interfaz:
- Diseño responsivo con archivos CSS dedicados como `test-responsive.css`.
- Uso de `localStorage` para el almacenamiento temporal de datos del usuario.
- Implementación de efectos visuales como barras de progreso (`progress-bar`).

### 2.2. Backend
Este proyecto utiliza **Firebase Firestore** como base de datos y almacenamiento en la nube.

#### Tecnologías Utilizadas:
- **Firebase Firestore** → Base de datos NoSQL para almacenar:
  - Información de usuarios que rinden los simulacros.
  - Resultados de los exámenes y reportes de desempeño.
  - Reclamos registrados en la plataforma.
- **Firebase Hosting** → Servidor para alojar y desplegar la página web.
- **JavaScript (Fetch API)** → Carga dinámica de los simulacros desde archivos JSON.

### 2.3. Manejo de Datos y Estado
El sistema almacena y gestiona datos tanto en el navegador del usuario como en Firestore:

#### LocalStorage (Almacenamiento Temporal en el Navegador)
- Guarda respuestas del usuario en el simulacro (`userAnswers`).
- Almacena los datos del examen seleccionado (`selectedExam`).
- Guarda los datos del usuario (`nombreAlumno`, `email`, `phone`).
- Se usa `examSent` para evitar que un examen sea enviado varias veces.

#### Firestore (Almacenamiento Permanente)
- Guarda los datos de los usuarios y los resultados del examen.
- Permite generar reportes y análisis de desempeño en la nube.

### 2.4. Visualización de Datos y Reportes
Para los reportes, la plataforma utiliza **Chart.js** para generar gráficos visuales:

- **Gráficos de barras** → Representación del porcentaje de aciertos en razonamiento verbal y razonamiento matemático.
- **Gráficos de líneas** → Evolución de puntajes en exámenes anteriores.
- **Tablas dinámicas** → Comparación de respuestas correctas e incorrectas.

Se emplean bibliotecas externas para la exportación de reportes:
- **`jspdf`** → Para generar reportes en formato PDF.
- **`html2canvas`** → Para capturar elementos de la página como imágenes.

### 2.5. Seguridad y Restricciones
- **Reglas de Firestore** → Solo usuarios autenticados pueden leer datos; la escritura está restringida en algunos casos.
- **Validaciones en el Frontend** → Se impide el envío de formularios sin datos completos.
- **Control de duplicados** → Se evita el doble envío de respuestas con `examSent`.

## 3️⃣ Estructura del Proyecto

La estructura del proyecto sigue una organización modular, separando los diferentes elementos en carpetas específicas dentro de la carpeta principal **Kuantum Landing**. A continuación, se detalla la distribución de los archivos y carpetas más relevantes:

```plaintext
/Kuantum Landing 
│── .firebase/                  # Configuración interna de Firebase 
│── index.html                  # Página principal 
│── public/                    # Carpeta principal accesible en el hosting 
│   │    
│   ├── pages/                  # Contiene páginas secundarias 
│   │   ├── login.html          # Página de inicio de sesión 
│   │   ├── reclamos.html       # Libro de reclamaciones 
│   │   ├── reporte.html        # Página de reportes 
│   │   ├── test.html           # Página del simulacro 
│   │    
│   ├── css/                    # Estilos de la página 
│   │   ├── global.css          # Estilos generales 
│   │   ├── index-responsive.css    # Estilos responsivos para index.html 
│   │   ├── reclamos.css       # Estilos específicos de reclamos.html 
│   │   ├── reporte.css         # Estilos para reporte.html 
│   │   ├── test-responsive.css     # Estilos responsivos del simulacro 
│   │   ├── test.css           # Estilos específicos del simulacro  
│   │    
│   ├── data/                   # Contiene archivos JSON de simulacros 
│   │   ├── examenPrueba.json       # Preguntas del examen 1 
│   │   ├── examenPrueba2.json      # Preguntas del examen 2 
│   │   ├── examenPrueba3.json      # Preguntas del examen 3 
│   │   ├── examenPrueba_images/    # Imágenes para el examen 1 
│   │   ├── examenPrueba2_images/   # Imágenes para el examen 2 
│   │   ├── examenPrueba3_images/   # Imágenes para el examen 3 
│   │    
│   ├── js/                     # Scripts de funcionalidad 
│   │   ├── firebase-config.js   # Configuración de Firebase 
│   │   ├── index.js            # Funcionalidades de la página principal 
│   │   ├── test.js             # Lógica del simulacro 
│   │    
│   ├── media/                  # Imágenes y gráficos usados en la web 
│   │   ├── icons/              # Íconos utilizados 
│   │    
│── favicon.png                 # Ícono del sitio web 
│── firebase.json               # Configuración de Firebase Hosting 
│── firestore.rules             # Reglas de Firestore 
│── firestore.indexes.json     # Índices de Firestore 
│── documentation.md            # Documento actual de documentación
```

### Descripción de las Carpetas Clave

- **`public/`** → Carpeta principal accesible para los usuarios en Firebase Hosting.
- **`css/`** → Contiene los archivos de estilos para las páginas.
- **`data/`** → Archivos JSON con preguntas y respuestas del simulacro.
- **`js/`** → Contiene los scripts principales de la plataforma.
- **`media/`** → Contiene imágenes, íconos y gráficos.
- **`pages/`** → Contiene las páginas secundarias del sitio.
- **Archivos en la raíz** → Configuración de Firebase, Firestore y documentación.




## 4️⃣ Descripción de las Funcionalidades

### 4.1 Página Principal (`index.html`)

La página principal contiene diversas secciones que estructuran la información y funcionalidades clave del sitio:

- **Sección Hero (`<section class="hero-section" id="home">`)**: Contiene el título principal y un botón de acción que dirige a los usuarios al simulacro.
- **Sección de Beneficios (`<section class="benefits-section" id="benefits">`)**: Muestra los beneficios clave de la plataforma utilizando tarjetas visuales.
- **Sección del Simulacro (`<section class="featured-simulation" id="simulationExam">`)**: Explica la importancia del simulacro y proporciona un botón de acceso.
- **Sección de Blog (`<section class="blog-section" id="blog">`)**: Contiene videos y enlaces a contenido educativo en YouTube.

#### 4.1.1 **Formulario de Registro**

La página principal cuenta con un **modal de registro (`#registration-modal`)** que se activa al hacer clic en el botón para acceder al simulacro. Este modal solicita datos esenciales como nombre, correo y teléfono. 

Un punto clave en este formulario es el **campo de selección de exámenes** (`<select id="exam" name="exam">`). Este elemento permite agregar fácilmente más exámenes JSON al sistema. Para ello, basta con incluir nuevas opciones dentro de este `<select>` y asegurarse de que los archivos JSON estén correctamente almacenados en la carpeta `/data/`.

El formulario también implementa validaciones antes de permitir que el usuario continúe.

#### 4.1.2 **Integración con Firestore**

La conexión con **Firestore** en esta página se encarga de almacenar los datos del usuario en la colección `usuarios`. Estos datos incluyen:
- Nombre y apellido
- Correo electrónico
- Número de teléfono
- Edad
- Examen seleccionado

Estos datos se almacenan de forma automática en Firestore tras el registro exitoso.

---

### 4.2 Simulacro de Examen (`test.html`)

La página del simulacro es donde los usuarios responden preguntas de exámenes previamente configurados en archivos JSON. Se diseñó para cargar dinámicamente las preguntas y almacenar las respuestas del usuario.

#### 4.2.1 **Carga Dinámica de Preguntas**

Las preguntas no están predefinidas en el HTML, sino que se generan dinámicamente desde un archivo JSON. Cuando el usuario selecciona un examen en el formulario de `index.html`, la plataforma carga el archivo JSON correspondiente desde la carpeta `/data/`.

El JSON debe cumplir con una estructura específica para evitar errores en la carga. Cada pregunta debe contener:
```json
{
      "type": "text-card",
      "category": "Razonamiento Verbal",
      "title": "Texto 1",
      "label": "Lee el siguiente texto y responde las preguntas 1-5",
      "content": "El Instituto Geofísico del Perú (IGP)...",
      "image": "../data/examenPrueba2_images/pregunta_1.jpg",
      "caption": "(Gráfico 1)",
      "content_after_image":"La etapa siguiente será...",
      "referencia": "Extraído de Examen UNMSM 2019-II"
},
{
   	 "type": "question",
    	 "number": 1,
    	 "category": "Razonamiento Verbal",
    	 "text": "¿Cuál es el significado de la palabra 'efímero'?",
   	 "options": ["Temporal", "Eterno", "Inmutable", "Perpetuo"],
    	 "answer": "A"
}

```
**Notas importantes:**
- El campo `type` debe estar presente para diferenciar preguntas de bloques de texto (`text-card`).
- El campo `answer` es **obligatorio**, ya que se usa para calcular los resultados en `reporte.html`.

#### 4.2.2 **Validaciones y Almacenamiento de Respuestas**

- Cada vez que un usuario selecciona una respuesta, esta se almacena en `localStorage` bajo la clave `userAnswers`.
- Se implementa un temporizador que fuerza la finalización del examen cuando el tiempo se agota.
- Antes de finalizar, el usuario debe confirmar su decisión a través de un modal.

---

### 4.3 Reporte de Resultados (`reporte.html`)

Una vez que el usuario completa el simulacro, se genera un informe detallado con sus resultados.

#### 4.3.1 **Generación de Reportes con Chart.js**

El informe utiliza **Chart.js** para mostrar gráficos estadísticos de desempeño:
- **Gráfico de barras:** Representa los aciertos en Razonamiento Verbal y Matemático.
- **Gráfico de línea:** Muestra la evolución del puntaje en relación con un promedio estimado.

Algunos datos dentro de los gráficos están basados en valores ficticios para simular un promedio grupal. Estos valores se encuentran en el script de `reporte.html` y pueden ajustarse en el futuro para calcularse dinámicamente con datos reales de Firestore.

#### 4.3.2 **Comparación de Respuestas**

La plataforma compara las respuestas almacenadas en `localStorage` con las respuestas correctas definidas en el JSON. Luego, se genera una tabla con el siguiente formato:
```
#  | Tú  | Clave
-----------------
1  | A   | A
2  | B   | C
3  | C   | C
```
Donde:
- `#` es el número de la pregunta.
- `Tú` muestra la respuesta seleccionada por el usuario.
- `Clave` muestra la respuesta correcta.

El puntaje total se calcula en base a los aciertos y se almacena en Firestore en la colección `examenes`.

---

## 5️⃣ Flujo de Usuario

El flujo de usuario describe la experiencia típica al utilizar la plataforma:

### 5.1 Registro e Ingreso
1. El usuario ingresa a `index.html`.
2. Completa el formulario de registro con sus datos personales y selecciona un examen.
3. Una vez completado el formulario, es redirigido automáticamente a `test.html` para iniciar el simulacro.

### 5.2 Realización del Simulacro
1. Se cargan dinámicamente las preguntas del JSON correspondiente al examen seleccionado.
2. El usuario responde cada pregunta interactuando con las opciones de respuesta.
3. El sistema guarda automáticamente las respuestas seleccionadas en `localStorage`.
4. Un temporizador controla la duración del examen y lo finaliza automáticamente cuando el tiempo se agota.
5. Antes de finalizar, el usuario debe confirmar su decisión en un modal emergente.

### 5.3 Visualización de Reportes
1. Tras completar el simulacro, el usuario es redirigido automáticamente a `reporte.html`.
2. Se generan gráficos estadísticos con **Chart.js** mostrando el desempeño del usuario.
3. Se comparan las respuestas del usuario con las correctas, generando una tabla detallada.
4. El sistema almacena los resultados en Firestore en la colección `examenes`.
5. El usuario puede visualizar su puntaje total y compararlo con un promedio estimado.

### 5.4 Presentación de Reclamaciones
1. Si el usuario tiene alguna objeción sobre el simulacro o el sistema, puede acceder a `reclamos.html`.
2. Completa el formulario de reclamaciones con los detalles de su queja.
3. El sistema verifica que todos los campos requeridos estén llenos antes de permitir el envío.
4. Una vez enviado, el reclamo se almacena en Firestore dentro de la colección `reclamos` para su posterior evaluación por parte del equipo de Kuantum.

---

## 6️⃣ Seguridad y Base de Datos

La plataforma **Kuantum Plataforma Web** utiliza **Firebase Firestore** como base de datos para almacenar información de usuarios, exámenes y reportes. Se han implementado medidas de seguridad para proteger los datos y garantizar el acceso autorizado.

### 6.1 **Reglas de Seguridad en Firestore**
Para evitar accesos no autorizados a la base de datos, se han configurado reglas en **Firestore**. Estas reglas permiten controlar quién puede leer o escribir información en la base de datos.

Ejemplo de las reglas implementadas:
```json
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /usuarios/{document=**} {
      allow read: if request.auth != null;
      allow write: if true;
    }
    
    match /examenes/{document=**} {
      allow read: if request.auth != null;
      allow write: if true;
    }
    
    match /reclamos/{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```
- **Los usuarios autenticados pueden leer datos de `usuarios` y `examenes` pero no modificarlos.**
- **Los reclamos pueden ser leídos y escritos solo por usuarios autenticados.**
- **El sistema está configurado para permitir la escritura de resultados sin autenticación en `examenes` (esto puede ser ajustado en el futuro si se requiere autenticación previa).**

### 6.2 **Manejo de Datos en Firestore**
Los datos se almacenan en colecciones separadas:

- **`usuarios`** → Almacena la información de los estudiantes que registran su participación en los simulacros.
- **`examenes`** → Guarda los resultados obtenidos en los simulacros.
- **`reclamos`** → Contiene las quejas enviadas por los usuarios a través del formulario de reclamaciones.

Cada colección almacena documentos estructurados de la siguiente forma:
```json
{
  "nombre": "Juan Pérez",
  "email": "juanperez@example.com",
  "telefono": "987654321",
  "examen": "Examen 1",
  "puntajeTotal": 80,
  "correctas": 40,
  "incorrectas": 20,
  "enBlanco": 0,
  "fecha": "2025-02-21"
}
```
Los resultados de los exámenes incluyen información sobre respuestas correctas, incorrectas y preguntas sin responder, permitiendo generar reportes detallados.

### 6.3 **Validaciones en el Frontend**
Para mejorar la seguridad, el sistema implementa validaciones antes de enviar datos a Firestore:
- **Validación de formularios** → Se verifica que los usuarios completen los campos requeridos antes de enviar los datos.
- **Evitar múltiples envíos de datos** → Se usa `localStorage` para registrar si los datos ya fueron enviados y prevenir duplicaciones.
- **Protección contra datos faltantes** → Se impide que los reportes se generen si no hay respuestas almacenadas.

## 7️⃣ Posibles Mejoras y Expansiones

Aunque la plataforma es completamente funcional, hay varias mejoras que podrían implementarse para optimizar la experiencia del usuario y expandir las funcionalidades de Kuantum.

### 7.1 **Autenticación de Usuarios**
Actualmente, la plataforma no cuenta con un sistema de autenticación. Una mejora clave sería implementar **Firebase Authentication** para que los usuarios puedan:
- Crear cuentas con correo y contraseña.
- Iniciar sesión con **Google** o **Facebook**.
- Guardar su historial de exámenes y progresos en una cuenta personalizada.

### 7.2 **Integración de una Pasarela de Pagos**
Para monetizar la plataforma, se podría agregar una **pasarela de pagos** con servicios como:
- **Culqi** o **MercadoPago** para pagos en Perú.
- **Stripe** o **PayPal** para pagos internacionales.
- Acceso a simulacros premium o cursos en línea después del pago.

### 7.3 **Expansión a una LMS (Learning Management System)**
Se podría convertir la plataforma en un sistema de gestión de aprendizaje (LMS), donde los usuarios puedan:
- Inscribirse en **cursos en línea**.
- Tener **material de estudio** y videos explicativos.
- Rendir **exámenes y simulacros personalizados** con seguimiento de avance.

### 7.4 **Optimización de Reportes con Datos Reales**
Actualmente, los reportes incluyen datos ficticios en algunos gráficos. Una mejora sería:
- Obtener **datos reales de otros exámenes** para generar comparaciones más precisas.
- Usar **inteligencia artificial** para sugerir áreas de mejora basadas en el desempeño del usuario.

### 7.5 **Modo Administrador para el Control de Datos**
Crear una interfaz para **administradores** que permita:
- **Gestionar exámenes** → Crear, editar o eliminar preguntas directamente desde la plataforma.
- **Ver estadísticas generales** → Analizar el desempeño de los usuarios en un panel de administración.
- **Manejar reclamos** → Revisar y dar seguimiento a las quejas enviadas por los usuarios.
