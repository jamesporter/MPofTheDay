/*
       Licensed to the Apache Software Foundation (ASF) under one
       or more contributor license agreements.  See the NOTICE file
       distributed with this work for additional information
       regarding copyright ownership.  The ASF licenses this file
       to you under the Apache License, Version 2.0 (the
       "License"); you may not use this file except in compliance
       with the License.  You may obtain a copy of the License at

         http://www.apache.org/licenses/LICENSE-2.0

       Unless required by applicable law or agreed to in writing,
       software distributed under the License is distributed on an
       "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
       KIND, either express or implied.  See the License for the
       specific language governing permissions and limitations
       under the License.
 */

package org.complexview.mps;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

import org.apache.cordova.*;

public class MPofTheDay extends CordovaActivity 
{
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        super.init();
        // Set by <content src="index.html" /> in config.xml
        super.loadUrl(Config.getStartUrl());
        //super.loadUrl("file:///android_asset/www/index.html")
    }
    
    @Override
    protected void onStart() {
    	super.onStart();
    	showNotification(getApplicationContext());
    	
    }

	private void showNotification(Context context) {
		NotificationManager nMan = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);

		
			Notification n = new Notification(R.drawable.notif,"MP of the Day" ,System.currentTimeMillis());
			
			n.flags |= Notification.FLAG_AUTO_CANCEL;
			n.flags |= Notification.FLAG_SHOW_LIGHTS;
			n.flags |= Notification.DEFAULT_SOUND;
			
			n.ledARGB = 0xff00ff00;
			n.ledOnMS = 200;
			n.ledOffMS = 200;
			
			Intent toLaunch = new Intent(context, MPofTheDay.class);
			PendingIntent intentBack = PendingIntent.getActivity(context, 0, toLaunch, 0);
			n.setLatestEventInfo(context, "MP of the Day", "Learn about your MP of the day", intentBack);
	
			nMan.notify(1,n);
		
	}
}

