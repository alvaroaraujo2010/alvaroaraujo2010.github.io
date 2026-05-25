import { Component, input } from '@angular/core';

@Component({
  selector: 'app-site-footer',
  standalone: true,
  templateUrl: './site-footer.component.html',
  styleUrl: './site-footer.component.scss',
})
export class SiteFooterComponent {
  readonly year = input.required<number>();
  readonly cvPath = input.required<string>();
}
