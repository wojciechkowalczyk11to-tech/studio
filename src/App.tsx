/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from 'react';
import { Download, Terminal, CheckCircle2, Rocket, Code2, ArrowRight } from 'lucide-react';
import { motion } from 'motion/react';

export default function App() {
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownload = () => {
    setIsDownloading(true);
    window.location.href = '/api/download';
    setTimeout(() => setIsDownloading(false), 2000);
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50 p-8 font-sans selection:bg-emerald-500/30">
      <div className="max-w-4xl mx-auto space-y-12">
        <header className="space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-sm font-medium border border-emerald-500/20">
            <CheckCircle2 className="w-4 h-4" />
            <span>Repository Analysis & Merge Complete</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-semibold tracking-tight">
            N.O.C Monorepo <span className="text-zinc-500">Ready for Deployment</span>
          </h1>
          <p className="text-zinc-400 text-lg max-w-2xl leading-relaxed">
            The source files from <code className="text-zinc-300 bg-zinc-900 px-1.5 py-0.5 rounded">AI-AGGREGATOR-UPDATED</code> and <code className="text-zinc-300 bg-zinc-900 px-1.5 py-0.5 rounded">nexus-omega-core</code> have been successfully merged into the root directory. The <code className="text-zinc-300 bg-zinc-900 px-1.5 py-0.5 rounded">docker-compose.yml</code> and <code className="text-zinc-300 bg-zinc-900 px-1.5 py-0.5 rounded">cloudbuild.yaml</code> files have been updated to reflect the new structure.
          </p>
        </header>

        <div className="grid md:grid-cols-2 gap-6">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 space-y-6"
          >
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 flex items-center justify-center border border-indigo-500/20">
              <Code2 className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
              <h3 className="text-xl font-medium mb-2">1. Download Source</h3>
              <p className="text-zinc-400 text-sm mb-6">
                Download the fully merged and fixed repository as a ZIP archive. This contains the updated backend, telegram bot, and infra configurations.
              </p>
              <button
                onClick={handleDownload}
                disabled={isDownloading}
                className="w-full flex items-center justify-center gap-2 bg-zinc-100 hover:bg-white text-zinc-900 px-4 py-3 rounded-xl font-medium transition-colors disabled:opacity-50"
              >
                <Download className="w-5 h-5" />
                {isDownloading ? 'Preparing ZIP...' : 'Download N.O.C Archive'}
              </button>
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-zinc-900/50 border border-zinc-800 rounded-2xl p-6 space-y-6"
          >
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 flex items-center justify-center border border-emerald-500/20">
              <Rocket className="w-6 h-6 text-emerald-400" />
            </div>
            <div>
              <h3 className="text-xl font-medium mb-2">2. Deploy to Cloud Run</h3>
              <p className="text-zinc-400 text-sm mb-6">
                Extract the downloaded archive, open your terminal in the extracted folder, and run the following command to deploy using Google Cloud Build:
              </p>
              <div className="bg-black border border-zinc-800 rounded-xl p-4 relative group">
                <code className="text-emerald-400 text-sm font-mono block overflow-x-auto">
                  gcloud builds submit --config cloudbuild.yaml .
                </code>
              </div>
            </div>
          </motion.div>
        </div>

        <section className="space-y-6 pt-8 border-t border-zinc-800/50">
          <h2 className="text-2xl font-medium flex items-center gap-2">
            <Terminal className="w-6 h-6 text-zinc-500" />
            Migration Summary
          </h2>
          <div className="grid gap-3">
            {[
              "Moved Source/nexus-omega-core/backend to root /backend",
              "Moved Source/nexus-omega-core/telegram_bot to root /telegram_bot",
              "Merged improvements from Source/AI-AGGREGATOR-UPDATED into /backend and /telegram_bot",
              "Updated docker-compose.yml paths to point to new root directories",
              "Generated cloudbuild.yaml for automated Cloud Run deployment"
            ].map((item, i) => (
              <div key={i} className="flex items-start gap-3 text-zinc-300 bg-zinc-900/30 p-4 rounded-xl border border-zinc-800/50">
                <ArrowRight className="w-5 h-5 text-zinc-600 shrink-0 mt-0.5" />
                <span>{item}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
