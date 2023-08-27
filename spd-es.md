# MateApp Timesheet #

## Resumen ##

Timesheet es una aplicación para geestionar el tiempo laboral de los recursos humanos. Si su organización genera ingresos merced a personas que ofrecen diversos tipos de servicios, Timesheet le permite acceder rápidamente a información relacionada con:

- **Productividad Individual:** Timesheet le ayuda a comprender la carga de trabajo de su grupo y de cada individuo, lo que permite un mejor respaldo en las decisiones empresariales.
- **Presupuestos de los Proyectos:** La mayoría de los contratos de servicios, ya sean únicos o recurrentes, se cotizan en función de los recursos estimados necesarios para completar el trabajo. Timesheet le ayuda a monitorear de manera efectiva la dedicación de recursos a los proyectos en relación a lo presupuestado.
- **Rentabilidad de los Clientes:** Las relaciones con los clientes rara vez son simples. Comprender los matices de la historia de sus negocios con cada cliente es crucial para la toma de decisiones. Timesheet ofrece un indicador adicional para este propósito: el balance histórico se la sumatoria de lo presupuestado en los proyectos del cliente, versus su resultado.

Timesheet se basa en tres principios:

1. **Carga de Horas Simple y de Confianza:** El trabajo se puede informar desde cualquier dispositivo utilizando un formulario extremadamente simple y multidispositivo. La filosofía detrás de Timesheet se basa en la relación de confianza con el empleado o contratista y el software no rastrea las actividades de las personas de manera alguna. Cada persona informa su dedicación de tiempo conforme a lo convenido con la dirección. 

2. **Hora como Unidad de Tiempo:** Timesheet utiliza la hora como la unidad de tiempo estándar. La hora es ls unidad universalmente aceptada en la planificación y presupuestación de recursos humanos. Por lo tanto, creemos que agregar fracciones de hora en la carga no tiene reelevancia para el resultado esperado de la aplicación.

3. **Períodos Mensuales:** Timesheet utiliza el mes como el período estándar para el análisis.

## Aplicación ##

### Perfiles ###

Cada usuario en la aplicación Timesheet se considera un recurso humano y tiene la capacidad de registrar horas. Sin embargo, los usuarios se dividen en tres perfiles:

- **Usuario Estándar:** El usuario estándar utiliza la aplicación únicamente para registrar horas y solamente puede editar y eliminar las hojas de tiempo generadas por ellos mismos.

- **Usuario Supervisor:** Además de las tareas de un usuario estándar, el supervisor puede acceder al módulo de gestión. Esto le brinda acceso a las secciones de análisis; así como crear, actualizar y eliminar otras entidades, excepto usuarios/recursos.

- **Usuario Administrador:** Además de las funciones de supervisor, al administrador accede al módulo de administración, lo que le permite crear, editar, desactivar o activar usuarios. También tienen acceso a la papelera del sistema y pueden realizar y descargar copias de seguridad.

### Entidades ###

Además del usuario/recurso, El diseño de Timesheet gira en torno a tres entidades principales:

- **Timesheet:** La hoja de tiempo sirve como la unidad fundamental de la aplicación. Su objetivo es simplificar la carga de datos solicitando solo información esencial: una fecha, el número de horas, si son en horario laboral o no laboral y un proyecto seleccionado de una lista. También se proporciona un campo opcional para notas. Los timesheets se registran para el usuario respectivo. Sin embargo, los supervisores tienen acceso a un formulario de creación similar en la sección de gestión/timesheet, lo que les permite generar timesheets para otros recursos. De manera consistente con otras aplicaciones de MateApp, los campos obligatorios de los formularios de carga son mínimas. Los usuarios no pueden registrar horas en fechas futuras, pero son libres de cargar horas para cualquier proyecto.

- **Proyectos:** Las horas se registran para proyectos específicos. Naturalmente, los proyectos están unívocamente relacionados a un Cliente. Los proyectos pueden ser pro única vez o recurrentes. A cada proyecto se le asigna un presupuesto global en horas (aunque no es mandatorio, es importante), un valor total para los proyectos por única vez o mensual para los proyectos recurrentes.

- **Clientes:** Un cliente abarca cualquier organización a la que se pueda asignar un proyecto. Sin embargo, no se admite la carga de horas en forma directa a un Cliente.

En lo que respecta a los Usuarios, un parámetro esencial (aunque no obligatorio) dentro del perfil del usuario que puede ser configurado por los administradores es el objetivo de mensual de asignación de horas.

## Uso de la Aplicación ##

### General ###

- Cada vista de detalle incluye un botón de edición rápida de notas, lo que permite la edición parcial del registro (específicamente las notas, sin editar todo el registro).

- Cada vista de lista es "responsive", lo que significa que mostrará menos columnas en pantallas más pequeñas, como los dispositivos móviles.

- Los encabezados de la mayoría de las vistas de lista incluyen una sección de filtro/búsqueda. Para las fechas, una lista desplegable ofrece un conveniente filtro por períodos de tiempo. Nota: Solo las opciones "Mes Corriente" y "Todo" incluyen elementos del mes actual. Todos los otros períodos concluyen en la última fecha del mes anterior al mes en curso. La búsqueda de texto se puede usar de manera independiente o en conjunto con el filtro de períodos.

### Uso Básico ###

Hay cinco opciones disponibles en la barra de navegación para operaciones básicas:

- **Mis Timesheets:** Esta es una vista de lista de las timesheets propias del usuario. Al cargarse, los elementos listados pertenecen al mes actual. Los usuarios pueden abrir los sus timesheets, y desde allí navegar al proyecto y cliente relacionados. Sin embargo, no pueden editar ni eliminar proyectos ni clientes, excepto las notas en el modo de edición rápida.

- **Registrar Timesheets** Esta opción permite a los usuarios agregar timesheets para si mismos.

- **Papelera:** Esta es la papelera del usuario.

- **Perfil:** Aquí, los usuarios pueden editar su información básica de perfil y cambiar su contraseña.

- **Cerrar Sesión:** La opción para salir del sistema.

### Módulo de Gestión ###

El menú de gestión, disponible para usuarios con privilegios de supervisor y administrador, se divide en cuatro secciones:

1. **Recursos:** La opción mostrará una tabla con el tiempo asignado y no asignado resumido para cada recurso en el período definido en el menú desplegable de filtro de fechas. El tiempo asignado se calcula utilizando las hojas de tiempo relevantes, mientras que el tiempo no asignado se deriva del Objetivo Mensual especificado en el perfil del usuario. Si el período mostrado comienza antes de la fecha de incorporación del recurso, el tiempo no asignado para ese usuario se calcula a partir de ese momento. Un botón en el encabezado de la tabla permite registrar timesheets para cualquier usuario. La hoja de detalle del usuario se puede acceder desde la tabla. Los perfiles de usuario no son editables en esta vista; solo la sección de administración permite tales cambios. Además de los detalles los detalles del usuario, se presenta otra tabla que resume los proyectos en los que el usuario ha participado dentro del rango de fechas seleccionado.

2. **Proyectos:** Esta opción muestra proyectos activos con el tiempo asignado resumido de todos los usuarios. Los proyectos inactivos (y por lo tanto, finalizados) se omiten del listado para evitar confusiones. Sin embargo, se puede utilizar una palabra clave especial, **@inactivo**, como término de búsqueda en el formulario de búsqueda para listarlos. Nuevos proyectos se pueden crear utilizando el botón en el encabezado de la tabla. La vista individual de cada proyecto es accesible a través de la tabla y proporciona información relevante del proyecto, notas del proyecto con capacidades de edición rápida y una tabla que resume el tiempo asignado a los recursos para el rango de fechas elegido. Las opciones completas de edición y borrado están disponibles en esta vista, aunque el botón de borrar solo se habilita si no existen timesheets asociadas.

## Plataforma ##

### Registro de Usuarios ###

MateApp utiliza direcciones de correo electrónico como nombres de usuario. El correo electrónico debe ser válido y accesible para el usuario, ya que se utiliza para el registro de usuarios y para recuperar contraseñas. MateApp ofrece los siguientes métodos de registro de usuarios:

- **Registro Manual:** Un administrador completa el formulario "Crear Usuario" y proporciona al usuario sus credenciales de inicio de sesión, o, siguiendo "mejores prácticas", solo proporciona el correo electrónico del nombre de usuario. Luego, el usuario crea una contraseña a través de la utilidad de recuperación de contraseñas.

- **Registro Propio con "En Espera":** Los usuarios se registran por sí mismos, pero sus perfiles permanecen inactivos hasta que un administrador los active manualmente.

- **Registro Propio con Restricción de Dominio:** Para organizaciones con un dominio de correo electrónico registrado, el registro propio está completamente automatizado, y el usuario se activa después de la confirmación del correo electrónico. Sin embargo, solo se aceptan correos electrónicos del dominio de la organización.

Los usuarios registrados a través de estos procesos se designan como Usuarios Estándar. Siempre es necesaria la intervención administrativa para elevar los privilegios al estado de supervisor o administrador.

### Eliminación de Elementos ###

MateApp incorpora una función de papelera. Los elementos eliminados por un usuario se conservan en la papelera del usuario hasta que se restauren o se eliminen permanentemente. Sin embargo, de manera predeterminada, MateApp nunca elimina completamente los registros. Las entradas eliminadas se almacenan en la Papelera de Administración del módulo de Administración. Este principio también se aplica a los elementos mantenidos en la papelera del usuario, lo que facilita la restauración iniciada por el administrador sin requerir acceso al perfil del usuario.