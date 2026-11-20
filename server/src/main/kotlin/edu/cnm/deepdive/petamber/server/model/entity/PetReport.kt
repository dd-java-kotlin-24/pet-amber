package edu.cnm.deepdive.petamber.server.model.entity

import jakarta.persistence.CascadeType
import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.EnumType
import jakarta.persistence.Enumerated
import jakarta.persistence.FetchType
import jakarta.persistence.GeneratedValue
import jakarta.persistence.GenerationType
import jakarta.persistence.Id
import jakarta.persistence.Index
import jakarta.persistence.JoinColumn
import jakarta.persistence.ManyToOne
import jakarta.persistence.OneToMany
import jakarta.persistence.OrderBy
import jakarta.persistence.PrePersist
import jakarta.persistence.Table
import org.hibernate.annotations.CreationTimestamp
import org.hibernate.annotations.UpdateTimestamp
import java.util.UUID
import kotlin.time.Instant

@Entity
@Table(
    name = "pet_report",
    indexes = [
        Index(columnList = "status"),
        Index(columnList = "last_seen_timestamp"),
        Index(columnList = "last_seen_latitude, last_seen_longitude")
    ]
)
class PetReport(

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "owner_id", nullable = false, updatable = false)
    var owner: UserProfile,

    @Column(name = "pet_name", nullable = false, length = 100)
    var petName: String,

    @Column(nullable = false, length = 50)
    var species: String,

    @Column(nullable = true, length = 100)
    var breed: String? = null,

    @Column(name = "color_markings", nullable = false, length = 255)
    var colorMarkings: String,

    @Column(name = "collar_description", nullable = true, length = 255)
    var collarDescription: String? = null,

    @Column(name = "is_microchipped", nullable = false)
    var isMicrochipped: Boolean = false,

    @Column(name = "photo_url", nullable = true, length = 1024)
    var photoUrl: String? = null,

    @Column(name = "last_seen_timestamp", nullable = false)
    var lastSeenTimestamp: Instant,

    @Column(name = "last_seen_latitude", nullable = false)
    var lastSeenLatitude: Double,

    @Column(name = "last_seen_longitude", nullable = false)
    var lastSeenLongitude: Double,

    @Column(name = "last_seen_address", nullable = true, length = 255)
    var lastSeenAddress: String? = null,

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    var status: Status = Status.ACTIVE_SEARCH,

    @Column(name = "resolution_notes", nullable = true, columnDefinition = "TEXT")
    var resolutionNotes: String? = null

) {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "pet_report_id", nullable = false, updatable = false)
    var id: Long? = null

    @Column(name = "external_key", nullable = false, updatable = false, unique = true)
    var externalKey: UUID? = null

    @Column(nullable = false, updatable = false)
    @CreationTimestamp
    open var created: Instant? = null

    @Column(nullable = false)
    @UpdateTimestamp
    open var updated: Instant? = null

    @OneToMany(
        mappedBy = "petReport",
        fetch = FetchType.LAZY,
        cascade = [CascadeType.ALL],
        orphanRemoval = true
    )
    @OrderBy("joined DESC")
    private val _squadMemberships: MutableList<SquadMembership> = mutableListOf()

    val squadMemberships: List<SquadMembership>
        get() = _squadMemberships.toList()

    @OneToMany(
        mappedBy = "petReport",
        fetch = FetchType.LAZY,
        cascade = [CascadeType.ALL],
        orphanRemoval = true
    )
    @OrderBy("sightingTimestamp DESC")
    private val _sightings: MutableList<Sighting> = mutableListOf()

    val sightings: List<Sighting>
        get() = _sightings.toList()

    @PrePersist
    fun generateFieldValues() {
        if (externalKey == null) {
            externalKey = UUID.randomUUID()
        }
    }

    enum class Status {
        ACTIVE_SEARCH,
        REUNITED,
        CLOSED
    }

}
