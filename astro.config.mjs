import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://votre-domaine.fr',
  output: 'static',
  integrations: [],
  build: {
    format: 'directory',
  },
  trailingSlash: 'always',
});
