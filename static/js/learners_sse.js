window.addEventListener('message', (event) => {
  evt_data = event.data;
  switch (evt_data.function) {
    case 'visibility':
      controlVisibility(pages = evt_data.data);
      break;
    default:
    //
  }
});

function controlVisibility(pages) {
  const menuItems = document.querySelectorAll('.page-control');
  for (let i = 0; i < menuItems.length; i++) {
    const menuItem = menuItems[i];

    let hidden = findHiddenValueByPageId(pages, menuItem.id);
    if (hidden) {
      $(menuItem).slideUp(250, () => {
        menuItem.classList.add('hidden');
      });
    } else {
      menuItem.classList.remove('hidden');
      $(menuItem).slideDown(400);
    }
  }
}
