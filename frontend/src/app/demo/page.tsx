import Image from 'next/image';
import Link from 'next/link';
import type { Metadata } from 'next';
import styles from './page.module.css';

export const metadata: Metadata = {
  title: 'Wordloom Demo',
  description: 'A recruiter-friendly overview of Wordloom, focused on search, async workflows, observability, and safe system evolution.',
  alternates: {
    canonical: '/demo',
  },
  openGraph: {
    title: 'Wordloom Demo',
    description: 'A recruiter-friendly overview of Wordloom, focused on search, async workflows, observability, and safe system evolution.',
    url: '/demo',
    siteName: 'Wordloom',
    type: 'website',
    images: [
      {
        url: '/demo/DEMO-main-content-model.png',
        width: 1600,
        height: 900,
        alt: 'Wordloom main content model',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Wordloom Demo',
    description: 'A backend-heavy knowledge platform focused on search, async workflows, observability, and safe system evolution.',
    images: ['/demo/DEMO-main-content-model.png'],
  },
  robots: {
    index: true,
    follow: true,
  },
};

const highlightCards = [
  {
    title: 'Backend-first architecture',
    body: 'FastAPI, PostgreSQL, Elasticsearch, and Next.js are organized around contracts, adapters, and stable boundaries rather than page-level glue code.',
  },
  {
    title: 'Outbox-driven async workflows',
    body: 'Projection workers, retries, replay paths, and low-cardinality failure reasons are treated as first-class engineering surfaces.',
  },
  {
    title: 'Search and read-model pipelines',
    body: 'The system separates write-side facts from read-side projections so search and timeline experiences can evolve safely over time.',
  },
  {
    title: 'Observability with evidence',
    body: 'Failure drills, CI artifacts, dashboards, and structured outputs are built to verify behavior instead of relying on ad hoc checks.',
  },
  {
    title: 'Safe migration thinking',
    body: 'Shadow runs, cutover windows, rollback paths, and operator-facing runbooks are designed as part of the implementation, not afterthoughts.',
  },
  {
    title: 'Security and tenant discipline',
    body: 'AuthContext, policy, audit, and tenant boundaries are treated as stable contracts that can extend into future cloud-facing integrations.',
  },
];

const quickFacts = [
  {
    label: 'Architecture posture',
    value: 'Backend-heavy',
    body: 'The project is designed around system boundaries, async work, and long-term operability instead of frontend-only polish.',
  },
  {
    label: 'Engineering focus',
    value: 'Evidence-driven',
    body: 'Drills, artifacts, and runbooks are part of the delivery model so system behavior can be verified instead of assumed.',
  },
  {
    label: 'Sharing mode',
    value: 'Static-friendly',
    body: 'This page and its core media can be opened without the backend API, which makes it safe to send as a first-look portfolio entry.',
  },
];

const stackGroups = [
  {
    label: 'Backend',
    items: 'Python, FastAPI, PostgreSQL',
  },
  {
    label: 'Search / Infra',
    items: 'Elasticsearch, Docker, projection workers',
  },
  {
    label: 'Frontend',
    items: 'Next.js, TypeScript, app-router UI',
  },
  {
    label: 'Engineering',
    items: 'GitHub Actions, observability, CI drills, evidence bundles',
  },
];

const screenshotCards = [
  {
    title: 'Product surfaces',
    description: 'The reading and authoring surface is designed around structured content instead of one-off documents.',
    src: '/demo/DEMO-1.png',
    width: 1600,
    height: 900,
  },
  {
    title: 'Search and structure',
    description: 'Search, hierarchy, and read views are tied back to projection-backed models and async processing.',
    src: '/demo/DEMO-2.png',
    width: 1600,
    height: 900,
  },
  {
    title: 'Text editor workflow',
    description: 'Editing is shown as a live content workflow rather than a static form, which better reflects the product feel of the system.',
    src: '/demo/DEMO-gif-1-2x.gif',
    width: 1200,
    height: 675,
  },
  {
    title: 'Engineering evidence',
    description: 'Operational verification is shown through drill outputs, evidence views, and system-facing diagnostics.',
    src: '/demo/DEMO-gif-2-2x.gif',
    width: 1200,
    height: 675,
  },
];

const footerLinks = [
  {
    label: 'GitHub',
    href: 'https://github.com/samuelhu324-dev/Wordloom',
  },
  {
    label: 'LinkedIn',
    href: 'https://www.linkedin.com/in/samuel-hu-08b4143a0/',
  },
  {
    label: 'Demo Video',
    href: '/demo/DEMO_VIDEO_1.mp4',
  },
  {
    label: 'README',
    href: 'https://github.com/samuelhu324-dev/Wordloom#readme',
  },
];

export default function DemoPage() {
  return (
    <main className={styles.page}>
      <section className={styles.hero}>
        <div className={styles.heroCopy}>
          <p className={styles.kicker}>Recruiter-friendly project front door</p>
          <h1 className={styles.heroTitle}>Wordloom</h1>
          <p className={styles.heroSubtitle}>
            A backend-heavy knowledge platform focused on search, async workflows, observability, and safe system evolution.
          </p>
          <p className={styles.heroBody}>
            This page is a concise front door for the product surface, the engineering shape behind it, and the kinds of backend and platform problems the project was designed to explore.
          </p>
          <div className={styles.heroActions}>
            <a className={styles.primaryAction} href="#demo-preview">View Demo</a>
            <a
              className={styles.secondaryAction}
              href="https://github.com/samuelhu324-dev/Wordloom"
              target="_blank"
              rel="noreferrer"
            >
              View GitHub
            </a>
          </div>
          <div className={styles.heroTags}>
            <span>Search-first architecture</span>
            <span>Outbox workflows</span>
            <span>Projection pipelines</span>
            <span>CI evidence</span>
          </div>
        </div>
        <div className={styles.heroVisual}>
          <div className={styles.visualCard}>
            <Image
              src="/demo/DEMO-main-content-model.png"
              alt="Wordloom main content model"
              width={1600}
              height={900}
              className={styles.visualImage}
              unoptimized
              priority
            />
            <p className={styles.visualCaption}>Main content model: Library to Bookshelf to Book to Block.</p>
          </div>
        </div>
      </section>

      <section className={`${styles.section} ${styles.factSection}`}>
        <div className={styles.factGrid}>
          {quickFacts.map((fact) => (
            <article key={fact.label} className={styles.factCard}>
              <p className={styles.factLabel}>{fact.label}</p>
              <h2 className={styles.factValue}>{fact.value}</h2>
              <p>{fact.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.sectionIntro}>
          <p className={styles.sectionEyebrow}>Project Overview</p>
          <h2>What the system is, why it was built, and what makes it different from a typical portfolio project.</h2>
        </div>
        <div className={styles.overviewGrid}>
          <article className={styles.overviewCard}>
            <h3>What it is</h3>
            <p>
              Wordloom is a full-stack knowledge platform that models content as structured entities rather than treating everything as flat documents.
            </p>
          </article>
          <article className={styles.overviewCard}>
            <h3>Why it exists</h3>
            <p>
              The project was built to show how product-facing features and backend-heavy engineering concerns can evolve together without losing control of contracts, operational clarity, or migration safety.
            </p>
          </article>
          <article className={styles.overviewCard}>
            <h3>What problem it tackles</h3>
            <p>
              It focuses on the hard part behind knowledge systems: search, asynchronous projections, failure handling, tenant-aware boundaries, and evidence-based change management instead of only surface-level CRUD flows.
            </p>
          </article>
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.sectionIntro}>
          <p className={styles.sectionEyebrow}>Key Engineering Highlights</p>
          <h2>Not a feature list. The emphasis is on the engineering posture behind the system.</h2>
        </div>
        <div className={styles.highlightGrid}>
          {highlightCards.map((card) => (
            <article key={card.title} className={styles.highlightCard}>
              <h3>{card.title}</h3>
              <p>{card.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="demo-preview" className={`${styles.section} ${styles.previewSection}`}>
        <div className={styles.sectionIntro}>
          <p className={styles.sectionEyebrow}>Demo Preview</p>
          <h2>A direct product snapshot with a public video file that opens without the backend.</h2>
        </div>
        <div className={styles.previewGrid}>
          <div className={styles.previewMedia}>
            <video className={styles.video} controls preload="metadata" poster="/demo/DEMO-main-content-model.png">
              <source src="/demo/DEMO_VIDEO_1.mp4" type="video/mp4" />
              Your browser does not support embedded video playback.
            </video>
          </div>
          <div className={styles.previewCopy}>
            <h3>Short product walkthrough</h3>
            <p>
              This preview is intentionally lightweight: a single public video asset, no auth requirement, and no runtime dependency on the backend API.
            </p>
            <p>
              That makes the page safe to share as a recruiter or hiring-manager first look while keeping the deeper product and engineering material one click away.
            </p>
            <div className={styles.previewActions}>
              <a className={styles.primaryAction} href="/demo/DEMO_VIDEO_1.mp4" target="_blank" rel="noreferrer">
                Watch Demo
              </a>
              <a className={styles.secondaryAction} href="https://github.com/samuelhu324-dev/Wordloom#readme" target="_blank" rel="noreferrer">
                Read README
              </a>
            </div>
          </div>
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.sectionIntro}>
          <p className={styles.sectionEyebrow}>Screenshots</p>
          <h2>Enough visual proof to explain the system, without turning the page into a gallery dump.</h2>
        </div>
        <div className={styles.screenshotGrid}>
          {screenshotCards.map((card) => (
            <figure key={card.title} className={styles.screenshotCard}>
              <Image
                src={card.src}
                alt={card.title}
                width={card.width}
                height={card.height}
                className={styles.screenshotImage}
                unoptimized
              />
              <figcaption>
                <strong>{card.title}</strong>
                <span>{card.description}</span>
              </figcaption>
            </figure>
          ))}
        </div>
      </section>

      <section className={styles.section}>
        <div className={styles.sectionIntro}>
          <p className={styles.sectionEyebrow}>Tech Stack</p>
          <h2>The stack is simple to scan, but the important part is how the pieces are organized.</h2>
        </div>
        <div className={styles.stackGrid}>
          {stackGroups.map((group) => (
            <article key={group.label} className={styles.stackCard}>
              <p className={styles.stackLabel}>{group.label}</p>
              <p className={styles.stackItems}>{group.items}</p>
            </article>
          ))}
        </div>
      </section>

      <footer className={styles.footer}>
        <div>
          <p className={styles.footerTitle}>Wordloom</p>
          <p className={styles.footerText}>
            A project about content systems, operational discipline, and building software that can evolve safely over time.
          </p>
        </div>
        <div className={styles.footerLinks}>
          {footerLinks.map((item) => (
            <Link
              key={item.label}
              href={item.href}
              className={styles.footerLink}
              target={item.href.startsWith('http') ? '_blank' : undefined}
              rel={item.href.startsWith('http') ? 'noreferrer' : undefined}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </footer>
    </main>
  );
}