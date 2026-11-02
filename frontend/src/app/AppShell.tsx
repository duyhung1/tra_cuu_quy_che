import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { useDocuments } from '../features/documents/useDocuments';
import { Icon } from '../shared/ui';

export function AppShell() {
  const { t } = useTranslation();
  const [navOpen, setNavOpen] = useState(false);
  const location = useLocation();
  const { data } = useDocuments();
  const ready = data?.counts.ready ?? 0;

  // Drawer < 1280 px: đồng bộ class lên body để CSS dùng chung
  useEffect(() => {
    document.body.classList.toggle('nav-open', navOpen);
    return () => document.body.classList.remove('nav-open');
  }, [navOpen]);

  // Đóng drawer khi đổi trang hoặc nhấn Esc
  useEffect(() => setNavOpen(false), [location.pathname]);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setNavOpen(false);
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);

  return (
    <>
      <a className="skip-link sr-only" href="#main">
        {t('app.skip')}
      </a>
      <header className="topbar">
        <button
          type="button"
          className="btn btn-ghost btn-icon menu-btn"
          aria-label={t('app.menu')}
          aria-expanded={navOpen}
          aria-controls="sidebar"
          onClick={() => setNavOpen((v) => !v)}
        >
          <Icon name="menu" />
        </button>
        <NavLink className="brand" to="/ask">
          <span className="brand-mark">
            <Icon name="chat" size={18} />
          </span>
          <span>{t('app.name')}</span>
        </NavLink>
        <span className="badge b-neutral hide-sm">{t('app.mvp')}</span>
      </header>
      {navOpen && <div className="scrim" onClick={() => setNavOpen(false)} />}
      <div className="layout">
        <nav className="sidebar" id="sidebar" aria-label={t('nav.ask')}>
          <div className="nav">
            <NavLink to="/ask" className={({ isActive }) => (isActive ? 'active' : '')}>
              <Icon name="chat" />
              <span>{t('nav.ask')}</span>
            </NavLink>
            <NavLink to="/documents" className={({ isActive }) => (isActive ? 'active' : '')}>
              <Icon name="file" />
              <span>{t('nav.documents')}</span>
              <span className="count" title={t('app.readyDocs', { count: ready })}>
                {ready}
              </span>
            </NavLink>
          </div>
          <div className="sidebar-foot">{t('app.footer')}</div>
        </nav>
        <main className="main" id="main">
          <Outlet />
        </main>
      </div>
    </>
  );
}
