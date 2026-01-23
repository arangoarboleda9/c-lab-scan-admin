# 🚀 C-LAB SCAN - Sistema de Diagnóstico Sistémico

Este ecosistema permite automatizar la recolección de diagnósticos empresariales, procesar los datos en tiempo real y generar dashboards de consultoría profesional listos para presentar.

---

## 🛠️ Componentes del Proyecto

### 1. Formulario Web (Frontend)
- **Tecnología:** HTML5, Tailwind CSS y JavaScript.
- **Función:** Captura respuestas de 24 preguntas divididas en 6 pilares estratégicos.
- **Despliegue:** [Vercel](https://vercel.com) (Carga ultra rápida).
- **Base de Datos:** Firebase Realtime Database.

### 2. Panel de Administración (Desktop App)
- **Tecnología:** Python 3.11 + CustomTkinter.
- **Función:** - Conecta con Firebase para extraer registros.
  - Cruza resultados con una **Matriz de Interpretación Integral**.
  - Genera gráficos radiales (Spider Charts) y de barras.
  - Genera diagnósticos, causas, recomendaciones y alcances automáticamente.
- **Conversión:** Compilado a `.EXE` mediante GitHub Actions.

---

## 📂 Estructura de Archivos
- `index.html`: Código de la encuesta web.
- `admin_app.py`: Script principal de la aplicación de escritorio.
- `logo.png`: Imagen corporativa incrustada en el software.
- `requirements.txt`: Lista de librerías para la ejecución del entorno.
- `.github/workflows/build.yml`: Automatización de compilación para Windows.

---

## ⚙️ Proceso de Extracción de Datos
1. **Envío:** El cliente finaliza la encuesta. Los datos se envían a la nube con un ID único.
2. **Recepción:** La App de escritorio consulta el nodo `calificaciones` en Firebase.
3. **Cálculo:** El sistema promedia las respuestas por categoría:
   - Estrategia y Alineación.
   - Procesos y Eficiencia.
   - Talento y Cultura.
   - Experiencia del Cliente.
   - Innovación y Agilidad.
   - Resultados y Sostenibilidad.
4. **Dashboard:** Se asigna un nivel (1 al 4) y se despliega la consultoría correspondiente de la matriz.

---

## 🚀 Instrucciones para Instalación (Windows)

1. **Descarga:** Ve a la pestaña **Actions** de este repositorio y descarga el último *Artifact* generado (`C-LAB-Admin-Windows`).
2. **Descomprimir:** Extrae el contenido del archivo ZIP.
3. **Ejecutar:** Abre `admin_app.exe`. 
   - *Nota: Si aparece el aviso de Windows SmartScreen, haz clic en "Más información" y luego en "Ejecutar de todas formas".*

---

## 🛠️ Desarrollo y Mantenimiento
Para realizar cambios en la aplicación de escritorio:
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`.
3. Para generar un nuevo ejecutable, simplemente sube los cambios a GitHub; el archivo `.yml` se encargará de crear el nuevo `.exe` automáticamente.

---
**Desarrollado por:** Alejandro Arango  
**Versión:** 1.0.0 (2026)
