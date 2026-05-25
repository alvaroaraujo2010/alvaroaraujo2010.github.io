import { Component, signal } from '@angular/core';
import { NAV_LINKS, PROFILE } from '../../core/data/portfolio.data';

@Component({
  selector: 'app-site-header',
  standalone: true,
  templateUrl: './site-header.component.html',
  styleUrl: './site-header.component.scss',
})
export class SiteHeaderComponent {
  readonly navLinks = NAV_LINKS;
  readonly cvPath = PROFILE.cvPath;
  readonly menuOpen = signal(false);

  toggleMenu(): void {
    this.menuOpen.update((open) => !open);
  }

  closeMenu(): void {
    this.menuOpen.set(false);
  }
}
