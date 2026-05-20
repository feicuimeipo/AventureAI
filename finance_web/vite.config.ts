import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';
import tailwindcss from '@tailwindcss/vite';
import vueJsx from '@vitejs/plugin-vue-jsx';

export default defineConfig(({ mode }) => {
  // 运行模式
  console.log('mode', mode)
  // 当前路径
  console.log('process.cwd()',process.cwd())
  const env=loadEnv(mode,process.cwd())
  console.log('env',env)

  const proxy = {
    '^/api/': {
      target: env.VITE_APP_HOST,
      changeOrigin: true,
      ws: true,
      rewrite: (path: any) => path.replace(/^\/api/, 'api'),
    },
  };

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
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
      },
    },
    css: {
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
        ...proxy
      }
    },
  };
});
