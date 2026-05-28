import { Component } from '@angular/core';
import { SiteHeaderComponent } from '../../layout/site-header/site-header.component';
import { SiteFooterComponent } from '../../layout/site-footer/site-footer.component';
import {
  CERTIFICATIONS,
  EDUCATION,
  EXPERIENCE,
  IMAGES,
  PROFILE,
  SKILLS,
  STATS,
  SUCCESS_CASES,
  TECH_STACK,
} from '../../core/data/portfolio.data';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [SiteHeaderComponent, SiteFooterComponent],
  templateUrl: './home.page.html',
  styleUrl: './home.page.scss',
})
export class HomePage {
  readonly profile = PROFILE;
  readonly stats = STATS;
  readonly techStack = TECH_STACK;
  readonly skills = SKILLS;
  readonly experience = EXPERIENCE;
  readonly successCases = SUCCESS_CASES;
  readonly education = EDUCATION;
  readonly certifications = CERTIFICATIONS;
  readonly images = IMAGES;
  readonly year = new Date().getFullYear();
}
