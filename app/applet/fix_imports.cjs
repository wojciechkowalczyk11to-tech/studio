const fs = require('fs');
const path = require('path');

function walk(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(function(file) {
    file = path.join(dir, file);
    const stat = fs.statSync(file);
    if (stat && stat.isDirectory()) { 
      results = results.concat(walk(file));
    } else { 
      if (file.endsWith('.py')) results.push(file);
    }
  });
  return results;
}

const files = walk(path.join(__dirname, 'repo_content/telegram_bot'));
files.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  if (content.includes('from telegram_bot.')) {
    content = content.replace(/from telegram_bot\./g, 'from ');
    fs.writeFileSync(file, content);
    console.log('Fixed imports in', file);
  }
});
