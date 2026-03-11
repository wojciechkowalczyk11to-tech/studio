const fs = require('fs');
const path = require('path');

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach(function(childItemName) {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else if (exists) {
    fs.copyFileSync(src, dest);
  }
}

const repoRoot = path.join(__dirname, 'repo_content');
const sourceNexus = path.join(repoRoot, 'Source', 'nexus-omega-core');
const sourceAggregator = path.join(repoRoot, 'Source', 'AI-AGGREGATOR-UPDATED');

const dirsToMove = ['backend', 'telegram_bot', 'infra'];

dirsToMove.forEach(dir => {
  const src = path.join(sourceNexus, dir);
  const dest = path.join(repoRoot, dir);
  if (fs.existsSync(src)) {
    console.log(`Copying ${src} to ${dest}`);
    copyRecursiveSync(src, dest);
  }
});

dirsToMove.forEach(dir => {
  const src = path.join(sourceAggregator, dir);
  const dest = path.join(repoRoot, dir);
  if (fs.existsSync(src)) {
    console.log(`Merging ${src} into ${dest}`);
    copyRecursiveSync(src, dest);
  }
});

const dockerComposePath = path.join(repoRoot, 'docker-compose.yml');
if (fs.existsSync(dockerComposePath)) {
  let content = fs.readFileSync(dockerComposePath, 'utf8');
  content = content.replace(/context: Source\/nexus-omega-core/g, 'context: .');
  // Update dockerfiles
  content = content.replace(/dockerfile: infra\/Dockerfile.backend/g, 'dockerfile: backend/Dockerfile');
  content = content.replace(/dockerfile: infra\/Dockerfile.bot/g, 'dockerfile: telegram_bot/Dockerfile');
  fs.writeFileSync(dockerComposePath, content);
  console.log('Updated docker-compose.yml');
}

console.log('Merge complete.');
