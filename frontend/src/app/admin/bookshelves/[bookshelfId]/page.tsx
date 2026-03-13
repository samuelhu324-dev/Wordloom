'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import { Breadcrumb } from '@/shared/ui';
import { BookMainWidget, type BookViewMode } from '@/widgets/book/BookMainWidget';
import { useBookshelf } from '@/features/bookshelf';
import { useLibrary } from '@/features/library';
import { useI18n } from '@/i18n/useI18n';
import styles from './page.module.css';

/**
 * Bookshelf Detail Page
 * Route: /admin/bookshelves/[bookshelfId]
 *
 * Displays bookshelf information and books within it
 * - Fetch bookshelf metadata by ID
 * - Fetch library info (through bookshelf)
 * - Display books using BookMainWidget (横向滚动卡片列表)
 * - Navigate to book detail
 */
export default function BookshelfDetailPage() {
  const params = useParams();
  const router = useRouter();
  const searchParams = useSearchParams();
  const bookshelfId = (params.bookshelfId as string) || '';
  const libraryId = searchParams.get('library_id') || '';
  const { t } = useI18n();
  const [resolvedLibraryId, setResolvedLibraryId] = useState(libraryId);

  useEffect(() => {
    if (libraryId) {
      setResolvedLibraryId(libraryId);
      try {
        localStorage.setItem('wl_active_library_id', libraryId);
      } catch {}
      return;
    }

    try {
      const activeLibraryId = localStorage.getItem('wl_active_library_id') || '';
      if (activeLibraryId) {
        setResolvedLibraryId(activeLibraryId);
        router.replace(`/admin/bookshelves/${bookshelfId}?library_id=${activeLibraryId}`);
        return;
      }

      for (let index = 0; index < localStorage.length; index += 1) {
        const key = localStorage.key(index);
        if (!key || !key.startsWith('wl_bookshelves_cache_')) continue;
        const raw = localStorage.getItem(key);
        if (!raw) continue;
        const parsed = JSON.parse(raw);
        const items = Array.isArray(parsed?.items) ? parsed.items : [];
        const match = items.find((item: any) => item?.id === bookshelfId && item?.library_id);
        if (match?.library_id) {
          setResolvedLibraryId(match.library_id);
          localStorage.setItem('wl_active_library_id', match.library_id);
          router.replace(`/admin/bookshelves/${bookshelfId}?library_id=${match.library_id}`);
          return;
        }
      }
    } catch {}
  }, [bookshelfId, libraryId, router]);

  // Fetch bookshelf
  const {
    data: bookshelf,
    isLoading: isBookshelfLoading,
    error: bookshelfError,
  } = useBookshelf(bookshelfId, resolvedLibraryId);

  // Fetch library (through bookshelf)
  const {
    data: library,
    isLoading: isLibraryLoading,
  } = useLibrary(bookshelf?.library_id || '');

  const isLoading = isBookshelfLoading || isLibraryLoading;
  const error = bookshelfError;

  const [viewMode, setViewMode] = useState<BookViewMode>('showcase');
  const [showCreate, setShowCreate] = useState(false);
  const [, setIsCreatePending] = useState(false);
  const [headerControlsEl, setHeaderControlsEl] = useState<HTMLDivElement | null>(null);

  if (isLoading) {
    return (
      <div className={styles.page}>
        <div className={styles.container}>
          <p>加载中...</p>
        </div>
      </div>
    );
  }

  if (error || !bookshelf) {
    return (
      <div className={styles.page}>
        <div className={styles.container}>
          <div className={styles.error}>
            <h2>无法加载书橱</h2>
            <p>Bookshelf ID: {bookshelfId}</p>
            <p className={styles.errorMessage}>{error?.message || '未知错误'}</p>
            <button onClick={() => router.back()} className={styles.backButton}>
              返回
            </button>
          </div>
        </div>
      </div>
    );
  }

  const handleSelectBook = (bookId: string) => {
    const suffix = resolvedLibraryId ? `?library_id=${resolvedLibraryId}` : '';
    router.push(`/admin/books/${bookId}${suffix}`);
  };

  return (
    <div className={styles.page}>
      <div className={styles.container}>
        <Breadcrumb
          items={[
            { label: t('bookshelves.library.breadcrumb.list'), href: '/admin/libraries' },
            library ? { label: library.name, href: `/admin/libraries/${library.id}` } : null,
            { label: bookshelf.name, active: true },
          ].filter(Boolean) as any}
        />

        {/* Header */}
        <div className={styles.header}>
          <div className={styles.headerRow}>
            <div className={styles.headerInfo}>
              <h1>{bookshelf.name}</h1>
              <p className={styles.description}>{bookshelf.description || '无描述'}</p>
            </div>
            <div className={styles.headerActionsMount} ref={setHeaderControlsEl} />
          </div>
        </div>

        {/* Books Section - 使用 BookMainWidget */}
        <div className={styles.section}>
          <BookMainWidget
            bookshelfId={bookshelfId}
            libraryId={library?.id || ''}
            library={library}
            onSelectBook={handleSelectBook}
            viewMode={viewMode}
            onViewModeChange={setViewMode}
            showCreate={showCreate}
            onShowCreateChange={setShowCreate}
            onCreatePendingChange={setIsCreatePending}
            headerPortalTarget={headerControlsEl}
          />
        </div>
      </div>
    </div>
  );
}
