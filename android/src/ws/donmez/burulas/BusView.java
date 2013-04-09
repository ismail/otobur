package ws.donmez.burulas;

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import javax.net.ssl.HttpsURLConnection;

import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONException;

import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Activity;
import android.content.Context;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;

public class BusView extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bus_view);

        final ListView listview = (ListView) findViewById(R.id.listView1);

        new DownloadScheduleTask().execute("https://raw.github.com/cartman/hackweek9/master/hours.json");
    }

    private class Bus {
        JSONArray backward;
        JSONArray forward;
        HashMap<String, ArrayList> hours;
        String url;
    }

   private class DownloadScheduleTask extends AsyncTask<String, Void, ByteArrayOutputStream> {
        protected ByteArrayOutputStream doInBackground(String... address) {
            ByteArrayOutputStream result = new ByteArrayOutputStream();
            byte[] buffer = new byte[4096];

            try {
                URL url =  new URL(address[0]);
                HttpsURLConnection urlConnection = (HttpsURLConnection) url.openConnection();
                urlConnection.setRequestMethod("GET");

                InputStream inputStream = urlConnection.getInputStream();

                int length  = 0;
                while ( (length = inputStream.read(buffer)) > 0 ) {
                    result.write(buffer, 0, length);
                }
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            return result;
         }

         protected void onPostExecute(ByteArrayOutputStream result) {
            Log.d("Burulas","Downloaded " + result.size() + " bytes.");
            parseSchedule(result);
        }
    }

    private void parseSchedule (ByteArrayOutputStream input)
    {
        HashMap<String, Bus> busMap = new HashMap<String, Bus>();

        try {
            JSONObject json = new JSONObject(input.toString());
            JSONArray keys = json.names();

            for (int i=0; i < keys.length(); ++i) {
                String entry = keys.getString(i);
                JSONObject entries = json.getJSONObject(entry);

                Bus bus = new Bus();
                try {
                    bus.backward = entries.getJSONArray("backward");
                    bus.forward = entries.getJSONArray("forward");
                } catch (JSONException e) {
                }

                bus.url = entries.getString("url");

                Log.d("Burulas", bus.url.toString());
            }
        } catch(JSONException e) {
            Log.d("Burulas", e.toString());
        }
    }
}
