import fs from 'node:fs';
fs.mkdirSync('dist-pages',{recursive:true});
fs.cpSync('dist','dist-pages',{recursive:true});
fs.copyFileSync('pages/_worker.js','dist-pages/_worker.js');
fs.copyFileSync('pages/_routes.json','dist-pages/_routes.json');
console.log('Pages bundle prepared: static assets + internal API binding');
