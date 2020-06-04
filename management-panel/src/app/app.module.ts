import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {HttpClientModule} from '@angular/common/http';
import {RouterModule, Routes} from '@angular/router';
import {MenuModule} from 'primeng/menu';
import {MegaMenuModule} from 'primeng';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {HomeComponent} from './home/home.component';
import {NotifyComponent} from './notify/notify.component';
import {FileUploadModule} from 'primeng/fileupload';
import {AddRepoComponent} from './add-repo/add-repo.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { AddBackupComponent } from './add-backup/add-backup.component';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';

const appRoutes: Routes = [
    {path: '', component: HomeComponent},
    {path: 'addRepo', component: AddRepoComponent},
    {path: 'notify', component: NotifyComponent},
    {path: 'addBackup', component: AddBackupComponent}
];

@NgModule({
    declarations: [AppComponent, HomeComponent, AddRepoComponent, NotifyComponent, AddBackupComponent],
    imports: [
        BrowserModule,
        HttpClientModule,
        RouterModule.forRoot(appRoutes),
        MenuModule,
        MegaMenuModule,
        BrowserAnimationsModule,
        FileUploadModule,
        FormsModule,
        ReactiveFormsModule,
      MatProgressSpinnerModule
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule {
}
