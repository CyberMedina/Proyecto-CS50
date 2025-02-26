# El Gusto CJ 🍝

Proyecto final desarrollado para el curso CS50. Se trata de una aplicación web que facilita la reserva de mesas en un restaurante. Los usuarios pueden registrarse y enviar solicitudes de reserva, mientras que los colaboradores del restaurante tienen la opción de aprobar o rechazar dichas solicitudes, notificando la decisión a través de correo electrónico.

## 📚 Tabla de Contenidos

- [Características](#-características)
- [Roles](#-roles)
- [Flujo de Proceso](#-flujo-de-proceso)
- [Tecnologías Usadas](#-tecnologías-usadas)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Contribuciones](#-contribuciones)
- [Contacto](#-contacto)

## 👥 Roles

- **Encargado de gestión de reservas**: Puede gestionar usuarios, ver reportes y administrar las reservas.
- **Recepcionista**: Maneja las reservas diarias y asiste en la organización de las mesas.
- **Cliente**: Puede registrarse, acceder a su perfil y gestionar sus datos y reservas.

## 🌟 Características

### Cliente:
- 🔹 Registro e inicio de sesión.
  <video src="https://github.com/user-attachments/assets/ed8d0463-66e6-485b-ae5b-71d27471d5a7" controls width="400"></video>

- 🔹 Realizar reservas.
  
  <video src="https://github.com/user-attachments/assets/56fbfad5-ea55-4f10-902f-50bb6cce6bae" controls width="400"></video>

### Colaboradores:
- 🔹 Modo claro y oscuro en la vista de administrador.
  
  <video src="https://github-production-user-asset-6210df.s3.amazonaws.com/114252123/416982681-b4c92b19-3c19-470b-ab66-6354b1fda6ed.mp4" controls width="600"></video>

### Encargado de gestión de reservas:
- 🔹 Aprobación y rechazo de reservas.
- 🔹 Validación de disponibilidad de mesas y sillas según su estado (ocupado/libre) o cantidad requerida.
- 🔹 Envío de correos electrónicos notificando la aprobación o rechazo de las reservas.

## 🛠️ Tecnologías Usadas

- **Frontend:** HTML, CSS, Bootstrap.
- **Backend:** Flask, MySQL.

## ⚙️ Instalación

1. Clona el repositorio:  
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   ```
2. Instala las dependencias:  
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el servidor:  
   ```bash
   flask run
   ```

## 🚀 Uso

- Para acceder como **Administrador**, usa `admin@example.com` y contraseña `123456`.
- Para acceder como **Usuario**, regístrate en la plataforma.

## 🤝 Contribuciones

Si deseas contribuir, por favor sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una rama con tu funcionalidad (`git checkout -b feature-nueva`).
3. Sube tus cambios (`git commit -m 'Agregada nueva feature'`).
4. Abre un Pull Request.

## 📬 Contacto

- ✉️ **Correo:** tuemail@example.com
- 💼 **LinkedIn:** [Tu Nombre](https://linkedin.com/in/tuusuario)
- 🐦 **Twitter:** [@tuusuario](https://twitter.com/tuusuario)

