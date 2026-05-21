// export interface ToastData {
//   icon: string;
//   text: string;
//   change: string;
//   isPositive: boolean;
// }

import { defineComponent } from 'vue'; // 确保你已经正确引入了Bootstrap的JS部分
import { Toast } from 'bootstrap';


export const showBootStrapToast = async (
  icon: string,
  text: string,
  change: string,
  isPositive: boolean,
  id: 'ToastForToken'
) => {
  const t = document.getElementById(id);
  // @ts-ignore
  document.getElementById(id + '_icon').innerText = icon;
  // @ts-ignore
  document.getElementById(id + '_Text').innerText = text;

  const ch = document.getElementById(id + '_change');

  // @ts-ignore
  ch.textContent = change;
  // @ts-ignore
  ch.style.color = isPositive
    ? 'var(--green)'
    : !isPositive && change.startsWith('-')
      ? 'var(--red)'
      : 'var(--text3)';

  t?.classList.add('show');
  // @ts-ignore
  const toastBootstrap = Toast.getOrCreateInstance(t);
  toastBootstrap.show();
  // @ts-ignore
  setTimeout(() => t.classList.remove('show'), 2800);
};


export default defineComponent({
  name: 'ToastForToken',
  setup(props: { id: string }) {
    return () => (
      <>
        <div class="toast" id={props.id}>
          <div class="toast-icon" id={`${props.id}_icon`}>
            {' '}
            🪙{' '}
          </div>
          <div>
            <div class="toast-text" id={`${props.id}_text`}>
              {' '}
              操作完成{' '}
            </div>
            <div class="toast-change" id={`${props.id}_change`}></div>
          </div>
        </div>
      </>
    );
  },
});