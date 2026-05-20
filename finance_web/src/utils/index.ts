export const toogleElementById = (elementId: string, display: boolean) => {
  const obj = document.getElementById(elementId);
  if (obj) {
    display ? (obj.style.display = 'block') : (obj.style.display = 'none');
  }
};
