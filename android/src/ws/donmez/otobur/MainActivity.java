package ws.donmez.otobur;

import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.zip.GZIPInputStream;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v4.app.FragmentActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

public class MainActivity extends FragmentActivity {
    public static class Bus {
        ArrayList<String> backward;
        ArrayList<String> forward;
        LinkedHashMap<String, ArrayList<String>> hours;
        String url;
        String name;
    }
    public static Bus currentBus;

    private static final int HTTP_CHUNK_SIZE = 8*1024;
    private static final int FILE_CHUNK_SIZE = 4*1024;
    private static HashMap<String, Bus> busMap;
    private static String jsonURL = "http://otobur.donmez.ws/data/schedule.json";
    private static String versionURL = "http://otobur.donmez.ws/data/schedule.version";
    private static String jsonVersion;
    private ListView lv;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main_activity);
        lv = (ListView) findViewById(android.R.id.list);

        lv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Object o = lv.getAdapter().getItem(position);
                String busName = o.toString();
                currentBus = busMap.get(busName);
                Intent intent = new Intent(MainActivity.this, DetailsActivity.class);
                startActivity(intent);
            }
        });

        getActionBar().setTitle(getString(R.string.bus_lines));

        if (!scheduleFileExists())
            new fetchScheduleTask().execute(jsonURL);
       else {
            parseScheduleFile();

            // See if auto-update is enabled
            SharedPreferences sharedPref = PreferenceManager.getDefaultSharedPreferences(this);
            Boolean autoUpdate = sharedPref.getBoolean("pref_auto_update", true);
            if (autoUpdate)
                new checkForUpdatesTask().execute(versionURL);
        }
    }

    private void updateBusList(ArrayList<String> busNames) {
        lv.setAdapter(new ArrayAdapter<String>(MainActivity.this,
                                                R.layout.custom_row_layout,
                                                busNames));
    }

    private boolean scheduleFileExists() {
        try {
            openFileInput("schedule.json");
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    private void parseScheduleFile() {
        StringBuilder jsonContent = new StringBuilder("");
        try {
            FileInputStream json = openFileInput("schedule.json");
            byte[] buffer = new byte[FILE_CHUNK_SIZE];

            while (json.read(buffer) != -1) {
                jsonContent.append(new String(buffer));
            }

        } catch (IOException e) {
            Log.d("Otobur", "Failed to write to schedule.json!");
            Log.d("Otobur", e.toString());
        }

        ArrayList<String> busNames = parseScheduleData(jsonContent.toString());
        updateBusList(busNames);
    }

    private ArrayList<String> parseScheduleData(String input) {
            busMap = new HashMap<String, Bus>();
            ArrayList<String> busNames = new ArrayList<String>();

            try {
                JSONObject json = new JSONObject(input);
                JSONArray keys = json.names();
                int length = keys.length() - 1; // Last key is version


                for (int i=0; i < length; ++i) {
                    JSONObject root = json.getJSONObject(Integer.toString(i));

                    String busName;
                    busName = root.getString("name");
                    busNames.add(busName);
                    Bus bus = new Bus();

                    jsonVersion = json.getString("version");

                    try {
                        ArrayList<String> backwardList = new ArrayList<String>();
                        JSONArray backwardArray = root.getJSONArray("backward");
                        for (int j=0; j < backwardArray.length(); ++j)
                            backwardList.add(backwardArray.getString(j));

                        bus.backward = backwardList;
                    } catch (JSONException ignored) {}

                    try {
                        ArrayList<String> forwardList = new ArrayList<String>();
                        JSONArray forwardArray = root.getJSONArray("forward");
                        for (int k=0; k < forwardArray.length(); ++k)
                            forwardList.add(forwardArray.getString(k));

                        bus.forward = forwardList;
                    } catch (JSONException ignored) { }

                    JSONObject hourArray = root.getJSONObject("hours");
                    JSONArray days = hourArray.names();
                    bus.hours = new LinkedHashMap<String, ArrayList<String>>();
                    for (int l=0; l < days.length(); ++l) {
                        String dayName = days.getString(l);
                        JSONArray hours = hourArray.getJSONArray(dayName);

                        ArrayList<String> hoursArray = new ArrayList<String>();
                        for (int m=0; m < hours.length(); ++m)
                            hoursArray.add(hours.getString(m));

                        bus.hours.put(dayName, hoursArray);
                    }

                    bus.name = busName;
                    bus.url = root.getString("url");
                    busMap.put(busName, bus);

                }
            } catch(JSONException e) {
                Log.d("Otobur", e.toString());
            }

            return busNames;
    }

    private ByteArrayOutputStream downloadToFile(String address, String output) {
            ByteArrayOutputStream result = new ByteArrayOutputStream();
            byte[] buffer = new byte[HTTP_CHUNK_SIZE];
            FileOutputStream fos = null;

            try {
                fos = openFileOutput(output, MODE_PRIVATE);
            } catch (IOException e) {
                Log.d("Otobur", "Failed to open " + output + " file!");
                Log.d("Otobur", e.toString());
            }

            try {
                URL url = new URL(address);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setRequestProperty("Accept-Encoding", "gzip, deflate");
                urlConnection.addRequestProperty("Cache-Control", "no-cache");
                urlConnection.setRequestMethod("GET");

                InputStream inputStream = urlConnection.getInputStream();
                String contentEncoding = urlConnection.getHeaderField("Content-Encoding");

                if (contentEncoding != null && contentEncoding.equalsIgnoreCase("gzip")) {
                    inputStream = new GZIPInputStream(inputStream);
                }

                int length;
                while ( (length = inputStream.read(buffer)) > 0 ) {
                    result.write(buffer, 0, length);
                    fos.write(buffer, 0, length);
                }
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            try {
                fos.close();
            } catch (IOException e) {
                Log.d("Otobur", "Failed to close " + output + " file!");
                Log.d("Otobur", e.toString());
            }

            return result;
        }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.main_activity, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.refresh:
                lv.setAdapter(null);
                new fetchScheduleTask().execute(jsonURL);
                return true;
            case R.id.settings:
                Intent intent = new Intent(MainActivity.this, SettingsActivity.class);
                startActivity(intent);
                return true;
        }

        return super.onOptionsItemSelected(item);
    }

    private class checkForUpdatesTask extends AsyncTask<String, Void, Boolean> {

        @Override
        protected Boolean doInBackground(String... urls) {
            ByteArrayOutputStream byteArray = downloadToFile(urls[0], "schedule.version");
            String version = byteArray.toString().trim();

            if (!version.equals(jsonVersion)) {
                Log.d("Otobur", "Need to update schedule. " + version + " != " + jsonVersion);
                return true;
            }
            else {
                Log.d("Otobur", "No need to update schedule. " + version + " == " + jsonVersion);
                return false;
            }
        }

        @Override
        protected void onPostExecute(Boolean updateNeeded) {
            if (updateNeeded)
                new updateScheduleTask().execute(jsonURL);
        }
    }

    private class updateScheduleTask extends AsyncTask<String, Void, ArrayList<String>> {
        @Override
        protected ArrayList<String> doInBackground(String... urls) {
            ByteArrayOutputStream input = downloadToFile(urls[0], "schedule.json");
            return parseScheduleData(input.toString());
        }

        @Override
        protected void onPostExecute(ArrayList<String> busNames) {
            updateBusList(busNames);

            Context context = getApplicationContext();
            CharSequence text = getString(R.string.schedule_updated);
            int duration = Toast.LENGTH_LONG;

            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }
    }

    private class fetchScheduleTask extends AsyncTask<String, Void, ArrayList<String>> {

        private final ProgressDialog dialog = new ProgressDialog(MainActivity.this);

        @Override
        protected void onPreExecute() {
            this.dialog.setMessage(getString(R.string.fetch_schedule));
            this.dialog.show();
        }

        @Override
        protected ArrayList<String> doInBackground(String... urls) {
            ByteArrayOutputStream input = downloadToFile(urls[0], "schedule.json");
            return parseScheduleData(input.toString());
        }

        @Override
        protected void onPostExecute(ArrayList<String> busNames) {
            if(this.dialog.isShowing())
                this.dialog.dismiss();

            updateBusList(busNames);
        }
    }
}
