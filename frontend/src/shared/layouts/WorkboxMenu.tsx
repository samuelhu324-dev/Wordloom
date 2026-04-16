"use client";
import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useI18n } from '@/i18n/useI18n';
import type { MessageKey } from '@/i18n/I18nContext';
import { AuthRole, useAuth } from '@/shared/auth';
import styles from './WorkboxMenu.module.css';

type MenuItem = {
  href: string;
  key: string;
  label?: string;
  labelKey?: MessageKey;
  roles?: AuthRole[];
};

const MENU_ITEMS: MenuItem[] = [
  { href: '/workbox/subscription', label: 'My Subscription', key: 'my-subscription', roles: ['member', 'admin', 'owner'] },
  { href: '/admin/subscriptions', label: 'Subscription Console', key: 'subscription-console', roles: ['admin', 'owner'] },
  { href: '/admin/libraries', labelKey: 'nav.libraries', key: 'libraries', roles: ['admin', 'owner'] },
  { href: '/admin/basement', labelKey: 'nav.basement', key: 'basement', roles: ['admin', 'owner'] },
  { href: '/admin/chronicle', labelKey: 'nav.chronicle', key: 'chronicle', roles: ['admin', 'owner'] },
  { href: '/admin/tags', labelKey: 'nav.tags', key: 'tags', roles: ['admin', 'owner'] },
];

export const WorkboxMenu: React.FC = () => {
  const { hydrated, session } = useAuth();
  const [mounted, setMounted] = useState(false);
  const [open, setOpen] = useState(false);
  const pathname = usePathname();
  const buttonRef = useRef<HTMLButtonElement>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const { t } = useI18n();

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleMouseEnter = () => setOpen(true);

  const handleMouseLeave = () => setOpen(false);

  const handleBlur = (event: React.FocusEvent<HTMLDivElement>) => {
    if (!event.currentTarget.contains(event.relatedTarget as Node | null)) {
      setOpen(false);
    }
  };

  // Keyboard: Esc to close
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && open) {
        setOpen(false);
        buttonRef.current?.focus();
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [open]);

  // Arrow navigation inside menu
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!open) return;
    const items = Array.from(menuRef.current?.querySelectorAll('[data-menuitem]') || []) as HTMLElement[];
    const currentIndex = items.indexOf(document.activeElement as HTMLElement);

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      const nextIndex = (currentIndex + 1) % items.length;
      items[nextIndex]?.focus();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      const prevIndex = (currentIndex - 1 + items.length) % items.length;
      items[prevIndex]?.focus();
    }
  };

  // Avoid hydration mismatch when language is resolved from client storage.
  const workboxLabel = mounted ? t('nav.workbox') : 'Workbox';
  const visibleItems = MENU_ITEMS.filter((item) => session && (!item.roles || item.roles.includes(session.role)));

  if (!hydrated || !session || visibleItems.length === 0) {
    return null;
  }

  return (
    <div
      className={styles.container}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onFocus={handleMouseEnter}
      onBlur={handleBlur}
    >
      <button
        ref={buttonRef}
        type="button"
        aria-haspopup="true"
        aria-expanded={open}
        aria-label={workboxLabel}
        className={styles.trigger}
        onClick={() => setOpen(o => !o)}
        onKeyDown={handleKeyDown}
        data-testid="workbox-trigger"
      >
        {workboxLabel} <span className={styles.caret} aria-hidden="true">▾</span>
      </button>
      {open && (
        <div
          ref={menuRef}
          role="menu"
          aria-label={workboxLabel}
          className={styles.panel}
          data-testid="workbox-menu"
        >
          <div className={styles.activeBar} />
          <ul className={styles.list}>
            {visibleItems.map(item => {
              const active = pathname?.startsWith(item.href);
              return (
                <li key={item.key} className={active ? styles.active : undefined}>
                  <Link
                    href={item.href}
                    role="menuitem"
                    tabIndex={-1}
                    data-menuitem
                    onClick={() => setOpen(false)}
                    className={styles.menuItem}
                  >
                    {item.labelKey ? t(item.labelKey) : item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
};
