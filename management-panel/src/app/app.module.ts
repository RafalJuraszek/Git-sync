import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import {HttpClientModule} from '@angular/common/http';
import {RouterModule, Routes} from '@angular/router';
import {MenuModule} from 'primeng/menu';
import {MenuItem} from 'primeng/api';
import {MegaMenuItem} from 'primeng/api';
import {MegaMenuModule} from 'primeng';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import { HomeComponent } from './home/home.component';
import {FileUploadModule} from 'primeng/fileupload';
import { AddRepoComponent } from './add-repo/add-repo.component';
import {ReactiveFormsModule} from '@angular/forms';


const appRoutes: Routes = [
  {path: '', component: HomeComponent},
  {path: 'addRepo', component: AddRepoComponent}
  // {path: 'users', component: UsersComponent },
  // {path: 'users/:id/:name', component: UsersComponent },
  // {path: 'servers', component: ServersComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    AddRepoComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(appRoutes),
    MenuModule,
    MegaMenuModule,
    BrowserAnimationsModule,
    FileUploadModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
