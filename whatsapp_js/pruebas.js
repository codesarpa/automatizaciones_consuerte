const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const {readdir} = require('fs/promises');
const path = require('path');

const config = require('./config.js');

const grupos = ['Prueba1', 'Prueba2', 'Prueba3', 'Prueba4', 'Prueba5', 'Prueba6', 'Prueba7', 'Prueba8', 'Prueba9', 'Prueba10', 'Prueba11', 'Prueba12', 'Prueba13', 'Michael','Santiago Torres'];
const carpetaImagenes = '//10.1.1.1/codesarpamoni/Escrutinio';

config.log('---------------------------------------------------------------');
config.log('SE INICIA EL PROCESO');



(async () => {
const nombreImagen = config.obtenerNombreImagen();
  if (!nombreImagen) {
    await config.log('⏱️ Horario no válido para el envío.');
    process.exit(0);
  }
  
  await config.log(`⏱️Se encontró el siguiente horario: ${nombreImagen}.`);

  const archivos = await readdir(config.path);
  const archivo = archivos.find(f => f === nombreImagen);

  if (!archivo) {
    const mensaje = `❌ Imagen ${nombreImagen} no encontrada`;
    await config.log(mensaje);
    await config.log("archivos encontrados en la carpeta:");
    await config.log("***********************************");
    for (const archivo of archivos){
      await config.log(archivo);
    }
    await config.log("***********************************");
    // await enviarCorreoError('Error envío imagen WhatsApp', mensaje);
    process.exit(1);
   }


  await config.log("Se encontró la imagen en el horario correspondiente: " + archivo);
  await config.log("Se procede a inicializar el cliente de WhatsApp");

  


  const client = new Client({
    authStrategy: new LocalAuth()
  });

  // await config.log("cliente de autenticacion: " + authStrategy);

  client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
  });

//   await config.log("cliente del qr: " + qrcode);


  client.on('ready', async () => {
    await config.log('✅ Cliente WhatsApp listo');
    const rutaCompleta = path.join(carpetaImagenes, archivo);
    await config.log("ruta completa de la imagen:" + rutaCompleta);
    const media = MessageMedia.fromFilePath(rutaCompleta);
    const chats = await client.getChats();

    for (const nombreGrupo of config.grupos) {
      try {
        const grupo = chats.find(chat => chat.isGroup && chat.name === nombreGrupo || chat.name === nombreGrupo);
        if (grupo || chats) {
          await client.sendMessage(grupo.id._serialized, media);
          await config.log(`📤 Imagen enviada a ${nombreGrupo}`);
        } else {
          const mensaje = `⚠️ Grupo "${nombreGrupo}" no encontrado.`;
          await config.log(mensaje);
          await config.enviarCorreo('Grupo no encontrado', mensaje);
        }
        await new Promise(resolve => setTimeout(resolve, 4000)); // espera entre envíos
      } catch (err) {
        const mensaje = `❌ Error enviando a ${nombreGrupo}: ${err.message}`;
        await config.log(mensaje);
        await config.enviarCorreo('Error envío grupo WhatsApp', mensaje);
      }
    }
    await config.log('✅ Proceso terminado con éxito');
    process.exit(0);
  });


  client.initialize();
})();
