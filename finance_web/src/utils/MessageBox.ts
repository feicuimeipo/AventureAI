


class MessageBox {
  constructor() {}

  public Alert(type: 'info' | 'error' | 'success' | 'warning', message: string) {
    const div = document.createElement('div');
    div.classList.add(...'fixed,inset-0,flex,items-center,justify-center,hidden,z-1'.split(','));
    div.style.backgroundColor = 'rgba(0, 0, 0, 0.6)';

    const bodyDiv = document.createElement('div');
    bodyDiv.classList.add(...'relative,border-0,text-white,rounded,z-100'.split(','));

    if (type == 'info') {
      bodyDiv.classList.add("bg-blue-500");
    }
    if (type == 'error') {
      bodyDiv.classList.add('bg-orange-500');
    }
    if (type == 'warning') {
      bodyDiv.classList.add('bg-yellow-500');
    }
    if (type == 'success') {
      bodyDiv.classList.add('bg-green-500');
    }

    bodyDiv.style.padding = '20px';
    bodyDiv.style.paddingRight = '50px';
    bodyDiv.style.margin = '10';
    div.appendChild(bodyDiv);

    const icon = document.createElement('span');
    icon.classList.add(...'inline-block p-10 align-middle text-xl'.split(' '));
    icon.style.paddingRight = '5px';
    if (type == 'info') {
      icon.innerHTML = '💡';
    }
    if (type == 'error') {
      icon.innerHTML = '⚠️ ';
    }
    if (type == 'warning') {
      icon.innerHTML = '❌';
    }
    if (type == 'success') {
      icon.innerHTML = '🚨 ';
    }
    bodyDiv.appendChild(icon);

    const content = document.createElement('div');
    content.classList.add(
      ...'inline-block px-10 align-middle text-white m-20 pt-0 pr-15 text-sm'.split(' ')
    );

    content.innerHTML = message
    bodyDiv.appendChild(content);

    const button = document.createElement('button');
    button.classList.add(
      ...'absolute top-0 right-0 mt-4 mr-6 leading-none bg-transparent text-2xl font-semibold outline focus:outline-none'.split(
        ' '
      )
    );
    button.style.width = '20px';
    button.style.height = '20px';
    button.style.lineHeight = '20x';
    button.style.marginRight = '20px';
    button.style.border = '0px';
    button.innerHTML = '&times;';
    bodyDiv.appendChild(button);

    document.body.appendChild(div);
    div.classList.remove('hidden');

    button.addEventListener('click', () => {
      div.classList.add('hidden');
      document.body.removeChild(div);
    });
  }

  public Error(message: string) {
    return this.Alert('error', message);
  }

  public Info(message: string) {
    return this.Alert('info', message);
  }

  public Warning(message: string) {
    return this.Alert('warning', message);
  }

  public Success(message: string) {
    return this.Alert('success', message);
  }
}

const messageBox = new MessageBox();
export default messageBox;