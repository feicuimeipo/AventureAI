import { Toast } from 'bootstrap';

export class BootstrapToast {
   id: string = 'myBootstrapToast';
   myToast: HTMLElement | null = null;

  constructor(id: string, message: string, type?: 'info' | 'warning' | 'success' | 'error') {
    if (!type) type = 'info';
    if (!document.getElementById(this.id)) {
      if (id && id !== 'myBootstrapToast') {
        this.id = id;
      }

      const div = document.createElement('div');
      div.classList.add(...'position-fixed bottom-0 end-0 p-3'.split(' '));
      div.style.zIndex = '99';
      div.style.position = 'fixed';

      const myToast = document.createElement('div');
      myToast.id = this.id;
      myToast.classList.add('toast');
      myToast.role = 'alert';
      myToast.ariaLive = 'assertive';
      myToast.ariaAtomic = 'true';
      div.appendChild(myToast);

      const headerDiv = document.createElement('div');
      headerDiv.classList.add('toast-header');
      headerDiv.innerHTML =
        '<strong class="me-auto">通知</strong>' +
        '<small class="text-muted"></small>' +
        ' <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>';
      myToast.appendChild(headerDiv);

      const bodyDiv = document.createElement('div');
      bodyDiv.innerHTML = message;
      myToast.appendChild(bodyDiv);
      document.body.appendChild(div);
      this.myToast = myToast;
    } else {
      this.myToast = document.createElement(this.id);
    }
  }

  public showToast(): void {
    // 获取 Toast 元素并初始化
    if (this.myToast!=null) {
      const toast = Toast.getOrCreateInstance(this.myToast, {
        autohide: false,
        delay: 0,
      });

      this.myToast.addEventListener('hidden.bs.toast', () => {
        this.myToast?.remove(); // 完全移除元素
      });
      toast.show();
    }

  }


}

