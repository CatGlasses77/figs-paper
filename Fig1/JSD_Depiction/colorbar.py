import matplotlib.pyplot as plt
import matplotlib as mpl
plt.rcParams['figure.dpi'] = 500
fig = plt.figure()
ax = fig.add_axes([0.05, 0.80, 0.9, 0.1])
plt.rcParams['figure.dpi'] = 500

cb = mpl.colorbar.ColorbarBase(ax, orientation='horizontal', cmap = plt.get_cmap('Blues'))

plt.axis('off')
plt.title("JSD", y = 1.5, fontsize = 40)
plt.savefig('just_colorbar', bbox_inches='tight', transparent = True)