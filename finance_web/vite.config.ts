import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';
import tailwindcss from '@tailwindcss/vite';
import vueJsx from '@vitejs/plugin-vue-jsx';

export default defineConfig(({ mode }) => {
  const env=loadEnv(mode,process.cwd())

  return {
    // 打包相对路径
    base: './',
    plugins: [
      vue(),
      tailwindcss(),
      vueJsx({
        transformOn: true,
        mergeProps: true,
      }),
    ],
    build: {
      rollupOptions: {
        output: {
          sourcemap: true,
        }
      }
    }
    ,
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
      },
    },
    css: {
      //关键配置：强制使用 PostCSS 而不是 LightningCSS
      transformer: 'postcss',
      postcss: './postcss.config.cjs',
      preprocessorOptions: {
        scss: {
          additionalData: `@use "@/styles/variables.scss" as *;`,
        },
      },
    },
    server: {
      host: true,
      port: 3000,
      cors: true,
      open: false,
      proxy: {
        '^/api/': {
          target: env.VITE_APP_HOST,
          changeOrigin: true,
          ws: true,
          // rewrite: (path) => path.replace(/^\/api/, ''),
        },
      }
    },
  };
});
