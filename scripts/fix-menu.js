/**
 * 构建前删除 menu 中值为 "#" 的占位项（用于覆盖 theme 默认菜单中不需要在主栏显示的条目）。
 * 在 Butterfly 的 deepMerge 之后运行（priority 0 < 1）。
 */
hexo.extend.filter.register('before_generate', () => {
  const menu = hexo.theme.config.menu;
  if (!menu) return;
  for (const key of Object.keys(menu)) {
    if (menu[key] === '#') {
      delete menu[key];
    }
  }
}, 0);
