# Gestión de Participantes

## Descripción
El proyecto **Gestión de Participantes** es una aplicación diseñada para facilitar la administración de participantes y sus respectivas participaciones en las reuniones semanales de los TJ. Proporciona una interfaz gráfica intuitiva y herramientas para gestionar datos de manera eficiente.

## Estructura del Proyecto
El proyecto está organizado en las siguientes carpetas y archivos principales:

- **core/**: Contiene la lógica principal del sistema, como la gestión de datos y el manejo de la caché.
  - `asignador.py`: Lógica para asignar participantes.
  - `datos_cache.py`: Manejo de datos en caché.
  - `gestor_datos.py`: Gestión de datos generales.

- **data/**: Almacena los datos utilizados por la aplicación.
  - `opciones_tipos.csv`: Configuración de tipos de opciones.
  - `participaciones.csv`: Registro de participaciones.
  - `participantes.csv`: Lista de participantes.
  - `logs/`: Carpeta para los registros de actividad.

- **recursos/**: Contiene los recursos gráficos como íconos y logotipos.

- **ui/**: Implementa la interfaz gráfica de usuario.
  - `menu_principal.py`: Menú principal de la aplicación.
  - `vista_asignador.py`: Vista para asignar participantes.
  - `vista_configuracion.py`: Configuración de la aplicación.
  - `vista_historial.py`: Historial de actividades.
  - `vista_participaciones.py`: Gestión de participaciones.
  - `vista_participantes.py`: Gestión de participantes.

- **config.py**: Archivo de configuración general.
- **main.py**: Punto de entrada principal de la aplicación.
- **version.json**: Archivo que contiene la versión actual del proyecto.

## Requisitos para ejecutar la aplicación empaquetada:
- Windows 10 o superior.

## Requisitos para ejecutar la aplicación clonando el repositorio
- Python 3.13 o superior.
- Librerías adicionales especificadas en el proyecto (si aplica).

## Instalación
### Opción 1: Descargar la aplicación empaquetada
1. Ve a la [sección de releases](https://github.com/AitorLcom/GestionParticipantes/releases) del repositorio.
2. Descarga la última versión disponible del archivo `.exe`.
3. Ejecuta el archivo descargado para iniciar la aplicación.

### Opción 2: Clonar el repositorio
1. Clona este repositorio:
   ```bash
   git clone https://github.com/AitorLcom/GestionParticipantes.git
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd GestionParticipantes
   ```
3. Instala las dependencias necesarias (si aplica):
   ```bash
   pip install -r requirements.txt
   ```

## Uso
Ejecuta el archivo principal para iniciar la aplicación:
```bash
python main.py
```

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request con tus sugerencias o mejoras.

## Licencia
Este proyecto está bajo la licencia Creative Commons Atribución-NoComercial 4.0 Internacional (CC BY-NC 4.0). Consulta el archivo `LICENSE` para más detalles.