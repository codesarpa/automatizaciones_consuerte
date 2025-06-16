const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const {readdir} = require('fs/promises');
const path = require('path');

const config = require('./config.js');

// const grupos = ['Prueba1', 'Prueba2', 'Prueba3', 'Prueba4', 'Prueba5', 'Prueba6', 'Prueba7', 'Prueba8', 'Prueba9', 'Prueba10', 'Prueba11', 'Prueba12', 'Prueba13', 'Michael','Santiago Torres'];
// const carpetaImagenes = '//10.1.1.1/codesarpamoni/Escrutinio';

config.log('---------------------------------------------------------------');
config.log('SE INICIA EL PROCESO');



(async () => {
const nombreImagen = config.obtenerNombreImagen();

if (!nombreImagen) {
  await config.log('⏱️ Horario no válido para el envío.');
  await config.enviarCorreo('HORARIO NO VALIDO', 'El horario actual no coincide con ningún horario de envío configurado.');
  process.exit(0);
}
await config.log(`⏱️Se encontró el siguiente horario: ${nombreImagen.fecha}.`);
await config.log(`⏱️ Se obtuvo el nombre de la imagen: ${nombreImagen.fecha}`);
await config.log(`⏱️ Ruta donde se va a mover la imagen: ${nombreImagen.rutaDestino}`);

  const archivos = await readdir(config.path_search);
  const archivo = archivos.find(f => f === nombreImagen.fecha);

  if (!archivo) {
    let mensaje = `❌ Imagen ${nombreImagen.fecha} no encontrada\n\n`;
    await config.log(mensaje);
    await config.log("Archivos encontrados en la carpeta:");
    await config.log("***********************************");
    mensaje += "Archivos encontrados en la carpeta:\n";
    mensaje += "***********************************\n";
    for (const archivo of archivos){
      await config.log(archivo);
      mensaje += archivo + "\n";
    }
    await config.log("***********************************");
    mensaje += "***********************************\n";
    await config.enviarCorreo('ERROR AL ENCONTRAR LA IMAGEN', mensaje);
    process.exit(1);
   }

  await config.log("Se encontró la imagen en el horario correspondiente: " + archivo);
  await config.log("Se procede a inicializar el cliente de WhatsApp");

  const client = new Client({
    authStrategy: new LocalAuth()
  });

  client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
  });

  client.on('ready', async () => {
    await config.log('✅ Cliente WhatsApp listo');
    const rutaCompleta = path.join(config.path_search, archivo);
    await config.log("ruta completa de la imagen:" + rutaCompleta);
    const media = MessageMedia.fromFilePath(rutaCompleta);
    const chats = await client.getChats();

    let mensaje = `📸 Enviando la imagen ${media.filename} a los grupos:\n\n`;
    // mensaje += media.filename+"\n";
    for (const nombreGrupo of config.grupos) {
      try {
        const grupo = chats.find(chat => chat.isGroup && chat.name === nombreGrupo || chat.name === nombreGrupo);
        if (grupo || chats) {
          await client.sendMessage(grupo.id._serialized, media);
          await config.log(`📤 Imagen enviada a ${nombreGrupo}`);
          mensaje += `✅ Imagen enviada correctamente a "${nombreGrupo}".\n`;
        } else {
          const mensaje = `⚠️ Grupo "${nombreGrupo}" no encontrado.`;
          await config.log(mensaje);
          await config.enviarCorreo('GRUPO NO ENCONTRADO', mensaje);
        }
        await new Promise(resolve => setTimeout(resolve, 4000)); // espera entre envíos
      } catch (err) {
        const mensaje = `❌ Error enviando a ${nombreGrupo}: ${err.message}`;
        await config.log(mensaje);
        await config.enviarCorreo('ERROR AL ENVIAR LA IMAGEN AL GRUPO', mensaje);
      }
    }
    mover_imagen = await config.moverImagen(rutaCompleta, nombreImagen.rutaDestino + nombreImagen.fecha);
    mensaje += `\n${mover_imagen}. \n\n Proceso terminado, gracias por su paciencia.`;
    await config.enviarCorreo('IMAGEN ENVIADA CORRECTAMENTE', mensaje);
    await config.log('✅ Proceso terminado con éxito');
    process.exit(0);
  });


  client.initialize();
})();
